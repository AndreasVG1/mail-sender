import smtplib
from email.message import EmailMessage
from jinja2 import Template
import os
from app.models import MailTemplate, MailSettings, MailLog
from app.utils.crypto import decrypt
from app import db
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import current_app

"""Stores a record of the sent email in the database."""
def log_mail(recipient: str, user_id: int, template_id: int) -> None:
    log = MailLog(
        recipient=recipient,
        timestamp=datetime.now(ZoneInfo("Europe/Tallinn")),
        user_id=user_id,
        template_id=template_id
    )
    db.session.add(log)
    db.session.commit()

"""Renders the HTML template with the provided context."""
def parse_template(template: str, context: dict = {}) -> str:
    html_template = Template(template)
    return html_template.render(context or {})

"""Attaches a file to the email if file path is valid."""
def add_file(msg: EmailMessage, file_path: str) -> EmailMessage:
    file_path = os.path.join(current_app.root_path, 'files', file_path)
    with open(file_path, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='pdf',
            filename=os.path.basename(file_path)
        )
    return msg

"""Builds the email message with HTML content and optional attachment."""
def set_msg(subject: str, sender: str, recipient: str, mail_content: str, file_path: str) -> EmailMessage:
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content("Failed to use template")
    msg.add_alternative(parse_template(mail_content, {"recipient": recipient}), subtype='html')

    message = add_file(msg, file_path)
    return message

"""Sends the email using SMTP and the provided template and settings."""
def send_mail(template: MailTemplate, to: str, settings: MailSettings) -> None:
    message = set_msg(template.title, settings.email_address, to, template.content_html, template.file_path)

    try:
        with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port) as smtp:
            smtp.login(settings.email_address, decrypt(settings.email_password))
            smtp.send_message(message)
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Failed to send email: {e}")