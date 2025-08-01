from flask import Blueprint, render_template
from flask_login import login_required, current_user

log = Blueprint("log", __name__)

@log.route("/logs")
@login_required
def logs() -> str:
    mail_logs = current_user.logs
    return render_template("logs.html", mail_logs=mail_logs)