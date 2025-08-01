from flask import Blueprint, request, redirect, url_for, render_template, current_app
from app import db
import os
from werkzeug.utils import secure_filename
from werkzeug.wrappers.response import Response
from flask_login import login_required, current_user
from ..models import MailTemplate

crud = Blueprint("crud", __name__)

@crud.route("/templates/new", methods=["GET", "POST"])
@login_required
def create() -> Response | str:
    UPLOAD_FOLDER = os.path.join(current_app.root_path, "files")

    user = current_user

    if request.method == "POST":
        title = request.form["templateName"]
        content_html = request.form["emailHtml"]
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
        return redirect(url_for("crud.all", popup=True, message="Template added successfully."))
    
    return render_template("new.html")

@crud.route("/templates/edit/<int:template_id>", methods=["GET", "POST"])
@login_required
def edit(template_id: int) -> Response | str:
    template = MailTemplate.query.filter_by(id=template_id, user_id=current_user.id).first()

    if not template:
        return redirect(url_for("crud.all"))

    if request.method == 'POST':
        template.title = request.form["templateName"]
        template.content_html = request.form["emailHtml"]

        # Handle file upload if new file provided
        file = request.files.get("file")
        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_folder = os.path.join(current_app.root_path, "files")
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            template.file_path = filename

        db.session.commit()
        return redirect(url_for("crud.all",  popup=True, message="Template updated successfully."))

    return render_template("edit.html", template=template)

@crud.route("/templates/delete/<int:template_id>", methods=["GET", "POST"])
@login_required
def delete(template_id: int) -> Response | str:
    template = MailTemplate.query.filter_by(id=template_id, user_id=current_user.id).first()

    if not template:
        return redirect(url_for("crud.all"))
    
    if request.method == 'POST':
        # Delete file if exists
        if template.file_path:
            file_path = os.path.join(current_app.root_path, "files", template.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Delete template from DB
        db.session.delete(template)
        db.session.commit()
        return redirect(url_for("crud.all", popup=True, message="Template deleted successfully."))
    
    return render_template("delete.html", template=template)

@crud.route("/templates/all")
@login_required
def all() -> Response | str:
    templates = current_user.templates
    return render_template("all_templates.html", templates=templates)