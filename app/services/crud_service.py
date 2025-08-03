from app import db
import os
from flask import current_app
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.utils import secure_filename
from ..models import MailTemplate
from bs4 import BeautifulSoup
import bleach

def clean_html_input(raw_html: str) -> str:
    return bleach.clean(raw_html, tags=["p", "br", "strong", "em", "ul", "ol", "li", "a"], strip=True)

def save_file(file: FileStorage | None) -> str | None:
    if file and file.filename:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.root_path, "files", filename))
        return filename
    return None

def delete_file(file_path: str) -> None:
    file = os.path.join(current_app.root_path, "files", file_path)
    if os.path.exists(file):
        os.remove(file)

def save_template(title: str, content: str, file_path: str | None, user_id: int) -> None:
    new_template = MailTemplate(
        title=title,
        content_html=clean_html_input(content),
        file_path=file_path,
        user_id=user_id
    )
    db.session.add(new_template)
    db.session.commit()

def update_template(template: MailTemplate, new_title: str, new_content: str, file: FileStorage | None) -> None:
    template.title = new_title
    template.content_html = clean_html_input(new_content)

    file_path = save_file(file)
    if file_path:
        if template.file_path:
            delete_file(template.file_path)
        
        template.file_path = file_path

    db.session.commit()

def delete_template(template: MailTemplate) -> None:
    if template.file_path:
            delete_file(template.file_path)

    db.session.delete(template)
    db.session.commit()
    return

def html_to_plain_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n")