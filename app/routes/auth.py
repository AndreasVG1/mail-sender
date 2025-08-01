from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import User
from werkzeug.wrappers.response import Response
from app.services.auth_service import (
    user_exists,
    create_user,
    create_mail_settings,
)

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login() -> Response | str:
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()
    
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register() -> Response | str:
    if request.method == "POST":
        username = request.form["username"]
        user_email = request.form["userEmail"]
        user_password = request.form["userPassword"]
        provider = request.form["provider"]
        account_email = request.form["accEmail"]
        account_password = request.form["accPassword"]

        if user_exists(username):
            flash("Username already exists")
        else:
            user = create_user(username, user_email, user_password)
            create_mail_settings(user.id, provider, account_email, account_password)
            return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("main.index"))




