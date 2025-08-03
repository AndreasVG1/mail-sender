from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email

class SendMailForm(FlaskForm):
    recipient = StringField("Recipient Email", validators=[DataRequired(), Email()])
    template_id = SelectField("Select Template", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Send Email")

    def validate_template_id(form, field): # type: ignore
        if field.data == -1:
            raise ValidationError("Please select a valid template.")
