from flask import Blueprint, render_template, request
from app.services.mail_service import send_mail, log_mail
from flask_login import login_required, current_user
from ..models import MailTemplate

main = Blueprint("main", __name__)

@main.route("/")
def index() -> str:
    return render_template("index.html")

@main.route("/send", methods=["GET", "POST"])
@login_required
def send() -> str:
    templates = MailTemplate.query.filter_by(user_id=current_user.id).all()

    if request.method == 'POST':
        to = request.form['recipient']
        template_id = request.form['template']
        template = MailTemplate.query.filter_by(id=template_id, user_id=current_user.id).first()

        if not template:
            return render_template("send.html", popup=False, temps=templates)

        send_mail(template, to, current_user.mail_settings)
        log_mail(to, current_user.id, template.id)
        return render_template("send.html", popup=True, temps=templates)

    return render_template("send.html", popup=False, temps=templates)

@main.route("/dashboard")
@login_required
def dashboard() -> str:
    user = current_user
    return render_template("dashboard.html", user=user)