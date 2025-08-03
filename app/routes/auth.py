from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User
from werkzeug.wrappers.response import Response
from app.forms.auth_forms import LoginForm
from app.forms.auth_forms import RegisterForm
from app.services.auth_service import (
    user_exists,
    create_user,
    create_mail_settings,
)

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
    
        if user and check_password_hash(user.password, password): # type: ignore
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("login.html", form=form)

@auth.route("/register", methods=["GET", "POST"])
def register() -> Response | str:
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        user_email = form.user_email.data
        user_password = form.user_password.data
        provider = form.provider.data
        account_email = form.acc_email.data
        account_password = form.acc_password.data

        if user_exists(username): # type: ignore
            flash("Username already exists")
        else:
            user = create_user(username, user_email, user_password) # type: ignore
            create_mail_settings(user.id, provider, account_email, account_password) # type: ignore
            return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("main.index"))




