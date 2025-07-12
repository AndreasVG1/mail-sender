import smtplib
from email.message import EmailMessage
from jinja2 import Template
from config import EMAIL_SERVER, EMAIL_PORT, EMAIL_USERNAME, EMAIL_PASSWORD


def parse_template(template: str) -> Template:
    with open(f'templates/{template}.html', 'r') as f:
        html_template = Template(f.read())

    return html_template.render()

def send_mail(template: str, to: str) -> None:
    msg = EmailMessage()
    msg['Subject'] = 'Juhend'
    msg['From'] = EMAIL_USERNAME
    msg['To'] = to
    msg.set_content("Malli kasutamine ebaõnnestus.")
    msg.add_alternative(parse_template(template), subtype='html')


    with open (f'files/{template}.pdf', 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='pdf',
            filename=template
        )

    with smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_PORT) as smtp:
        smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        smtp.send_message(msg)