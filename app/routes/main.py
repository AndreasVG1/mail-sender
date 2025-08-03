from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug import Response
from app.services.mail_service import send_mail, log_mail
from flask_login import login_required, current_user
from ..models import MailTemplate
from app.forms.send_mail_form import SendMailForm

main = Blueprint("main", __name__)

@main.route("/")
def index() -> str:
    return render_template("index.html")

@main.route("/send", methods=["GET", "POST"])
@login_required
def send() -> str | Response:
    form = SendMailForm()

    templates = MailTemplate.query.filter_by(user_id=current_user.id).all()   
    form.template_id.choices = [(-1, "-- Select a template --")] + [(t.id, t.title) for t in templates] # type: ignore

    if request.method == 'POST' and form.validate_on_submit():
        to = form.recipient.data
        template_id = form.template_id.data
        template = MailTemplate.query.filter_by(id=template_id, user_id=current_user.id).first()

        if not template:
            return render_template("send.html", form=form)

        send_mail(template, to, current_user.mail_settings) # type: ignore
        log_mail(to, current_user.id, template.id) # type: ignore
        flash("Email sent successfully!", "success")
        return redirect(url_for("main.send"))

    return render_template("send.html", form=form)

@main.route("/dashboard")
@login_required
def dashboard() -> str:
    user = current_user
    return render_template("dashboard.html", user=user)