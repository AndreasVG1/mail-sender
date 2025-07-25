from flask import Blueprint, request, session, redirect, url_for, render_template, current_app
from app import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from ..models import MailTemplate

crud = Blueprint("crud", __name__)

@crud.route("/templates/new", methods=["GET", "POST"])
@login_required
def create_template():
    UPLOAD_FOLDER = os.path.join(current_app.root_path, "files")

    user = current_user

    if request.method == "POST":
        title = request.form["templateName"]
        content_html = request.form["emailContent"]
        file = request.files.get("file")

        file_path = None
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            file_path = filename

        # Save to DB
        new_template = MailTemplate(
            title=title,
            content_html=content_html,
            file_path=file_path,
            user_id=user.id
        )
        db.session.add(new_template)
        db.session.commit()
        return redirect(url_for("main.dashboard"))
    
    return render_template("new.html")

@crud.route("/templates/all")
@login_required
def all_templates():
    user = current_user
    templates = user.templates
    return render_template("all_templates.html", templates=templates)