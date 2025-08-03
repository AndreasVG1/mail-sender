from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3)])
    user_email = StringField('Your Email', validators=[DataRequired(), Email()])
    user_password = PasswordField('Your Password', validators=[DataRequired()])
    
    provider = SelectField('Email Provider', choices=[
        ('zone', 'Zone'),
        ('gmail', 'Gmail'),
        ('outlook', 'Outlook')
    ], validators=[DataRequired()])
    
    acc_email = StringField('Email Account Address', validators=[DataRequired(), Email()])
    acc_password = PasswordField('Email Account Password', validators=[DataRequired()])
    
    submit = SubmitField('Register')
