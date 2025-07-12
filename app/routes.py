from flask import Blueprint, render_template, request
from app.mail_service import send_mail
import os

main = Blueprint("main", __name__)

def getTemplates() -> list[str]:
    templates: list[str] = []
    for name in os.listdir('files/'):
        templates.append(os.path.splitext(name)[0])
    return(templates)


@main.route("/", methods=["GET", "POST"])
def index():
    templates: list[str] = getTemplates()
    if request.method == 'POST':
        to = request.form['recipient']
        template = request.form['template']
        send_mail(template, to)
        return render_template("index.html", popup=True, temps=templates)

    return render_template("index.html", popup=False, temps=templates)

