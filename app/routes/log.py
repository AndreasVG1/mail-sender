from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from app.models import MailLog

log = Blueprint("log", __name__)

@log.route("/logs")
@login_required
def logs() -> str:
    page = request.args.get('page', 1, type=int)
    per_page = 10
    from app.models import MailLog
    mail_logs_query = MailLog.query.filter_by(user_id=current_user.id).order_by(MailLog.timestamp.desc())
    pagination = mail_logs_query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template("logs.html", mail_logs=pagination.items, pagination=pagination)