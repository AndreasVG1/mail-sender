from werkzeug.security import generate_password_hash
from app.utils.crypto import encrypt
from app.models import User, MailSettings
from app import db

PROVIDER_MAP = {
    "zone": ("smtp.zone.eu", 465),
    "gmail": ("smtp.gmail.com", 587),
    "outlook": ("smtp.office365.com", 587),
}

def get_provider_info(provider: str) -> tuple[str, int]:
    return PROVIDER_MAP.get(provider, ("smtp.office365.com", 587))


def user_exists(username: str) -> bool:
    return User.query.filter_by(username=username).first() is not None


def create_user(username: str, email: str, password: str) -> User:
    user = User(username=username, email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user


def create_mail_settings(user_id: int, provider: str, email: str, password: str) -> None:
    smtp_server, smtp_port = get_provider_info(provider)
    settings = MailSettings(
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        use_tls=True,
        email_address=email,
        email_password=encrypt(password),
        user_id=user_id
    )
    db.session.add(settings)
    db.session.commit()