from flask import Blueprint, render_template, request, session, redirect, url_for
from app.mail_service import send_mail
from flask_login import login_required, current_user
from ..models import User
# from app import db
import os

main = Blueprint("main", __name__)

def getTemplates() -> list[str]:
    templates: list[str] = []
    for name in os.listdir('app/files/'):
        templates.append(os.path.splitext(name)[0])
    return(templates)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/send", methods=["GET", "POST"])
def send():
    templates: list[str] = getTemplates()
    if request.method == 'POST':
        to = request.form['recipient']
        template = request.form['template']
        send_mail(template, to)
        return render_template("send.html", popup=True, temps=templates)

    return render_template("send.html", popup=False, temps=templates)

@main.route("/dashboard")
@login_required
def dashboard():
    user = current_user
    return render_template("dashboard.html", user=user)