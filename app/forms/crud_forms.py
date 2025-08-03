from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class TemplateForm(FlaskForm):
    template_name = StringField("Template Name", validators=[DataRequired()])
    file = FileField("Attach PDF", validators=[FileAllowed(['pdf'], 'PDF only!')])
    submit = SubmitField("Save")

class DeleteForm(FlaskForm):
    submit = SubmitField("Delete")
