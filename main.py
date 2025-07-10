from dotenv import load_dotenv
from jinja2 import Template
import os
import smtplib
from email.message import EmailMessage

load_dotenv()
USERNAME = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")

SMTP_SERVER = 'smtp.zone.eu'
SMTP_PORT = 465
def send_mail(template, to):
    with open(f'templates/aknajuhend.html', 'r') as f:
        template = Template(f.read())

    html_body = template.render()

    msg = EmailMessage()
    msg['Subject'] = 'Aknaroboti kasutamise juhend'
    msg['From'] = USERNAME
    msg['To'] = to
    msg.set_content("Malli kasutamine ebaõnnestus.")
    msg.add_alternative(html_body, subtype='html')


    with open ('files/aknajuhend.pdf', 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype='application',
            subtype='pdf',
            filename='aknajuhend'
        )

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(USERNAME, PASSWORD)
        smtp.send_message(msg)

    return "Message Sent"