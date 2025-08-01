from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.wrappers.response import Response
from flask_login import login_required, current_user
from ..models import MailTemplate
from app.services.crud_service import (
    save_file, 
    save_template, 
    update_template,
    delete_template, 
    html_to_plain_text)

crud = Blueprint("crud", __name__)

@crud.route("/templates/new", methods=["GET", "POST"])
@login_required
def create() -> Response | str:
    if request.method == "POST":
        title = request.form["templateName"]
        content_html = request.form["emailHtml"]
        file_path = save_file(request.files.get("file"))
        
        save_template(title, content_html, file_path, current_user.id)
        return redirect(url_for("crud.all", popup=True, message="Template added successfully."))
    
    return render_template("new.html")

@crud.route("/templates/edit/<int:template_id>", methods=["GET", "POST"])
@login_required
def edit(template_id: int) -> Response | str:
    template = MailTemplate.query.filter_by(id=template_id, user_id=current_user.id).first()

    if not template:
        return redirect(url_for("crud.all"))

    if request.method == 'POST':
        new_title = request.form["templateName"]
        new_content = request.form["emailHtml"]
        file = request.files.get("file")
        update_template(template, new_title, new_content, file)
    
        return redirect(url_for("crud.all",  popup=True, message="Template updated successfully."))

    plain_text = html_to_plain_text(template.content_html)
    return render_template("edit.html", template=template, plain_text=plain_text)

@crud.route("/templates/delete/<int:template_id>", methods=["GET", "POST"])
@login_required
def delete(template_id: int) -> Response | str:
    template = MailTemplate.query.filter_by(id=template_id, user_id=current_user.id).first()

    if not template:
        return redirect(url_for("crud.all"))
    
    if request.method == 'POST':
        delete_template(template)
        return redirect(url_for("crud.all", popup=True, message="Template deleted successfully."))
    
    return render_template("delete.html", template=template)

@crud.route("/templates/all")
@login_required
def all() -> Response | str:
    templates = current_user.templates
    return render_template("all_templates.html", templates=templates)