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


def log_mail(recipient: str, user_id: int, template_id: int) -> None:
    log = MailLog(
        recipient=recipient,
        timestamp=datetime.now(ZoneInfo("Europe/Tallinn")),
        user_id=user_id,
        template_id=template_id
    )
    db.session.add(log)
    db.session.commit()

def parse_template(template: str, context: dict = {}) -> str:
    html_template = Template(template)
    return html_template.render(context or {})

def send_mail(template: MailTemplate, to: str, settings: MailSettings) -> None:
    msg = EmailMessage()
    msg['Subject'] = template.title
    msg['From'] = settings.email_address
    msg['To'] = to
    msg.set_content("Failed to use template")
    msg.add_alternative(parse_template(template.content_html, {"recipient": to}), subtype='html')

    file_path = os.path.join(current_app.root_path, 'files', template.file_path)

    with open (file_path, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='pdf',
            filename=os.path.basename(template.file_path)
        )

    with smtplib.SMTP_SSL(settings.smtp_server, settings.smtp_port) as smtp:
        smtp.login(settings.email_address, decrypt(settings.email_password))
        smtp.send_message(msg)
    print("Email sent!")