from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, MailSettings
from app.utils.crypto import encrypt
from werkzeug.wrappers.response import Response

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
        user_password = generate_password_hash(request.form["userPassword"])

        provider = request.form["provider"]
        account_email = request.form["accEmail"]
        account_password = encrypt(request.form["accPassword"])
        
        provider_map: dict[str, tuple[str, int]] = {
            "zone": ("smtp.zone.eu", 465),
            "gmail": ("smtp.gmail.com", 587),
            "outlook": ("smtp.office365.com", 587),
        }

        provider_info = provider_map.get(provider, ("smtp.office365.com", 587))
        smtp_server = provider_info[0]
        smtp_port = provider_info[1]

        if User.query.filter_by(username=username).first():
            flash("Username already exists")
        else:
            new_user = User(username=username, email=user_email, password=user_password)
            db.session.add(new_user)
            db.session.commit()

            settings = MailSettings(
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                use_tls=True,
                email_address=account_email,
                email_password=account_password,
                user_id=new_user.id
            )
            db.session.add(settings)
            db.session.commit()
            return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("main.index"))




