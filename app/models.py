from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, DateTime
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = "users"

    def __init__(self, username, email, password):
        self.username=username
        self.email=email
        self.password=password

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    templates: Mapped[list["MailTemplate"]] = relationship(back_populates="user")
    logs: Mapped[list["MailLog"]] = relationship(back_populates="user")
    mail_settings: Mapped["MailSettings"] = relationship(back_populates="user", uselist=False)

class MailTemplate(db.Model):
    __tablename__ = "templates"

    def __init__(self, title, content_html, file_path, user_id):
        self.title=title
        self.content_html=content_html
        self.file_path=file_path
        self.user_id=user_id

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content_html: Mapped[str] = mapped_column(Text, nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="templates")
    logs: Mapped[list["MailLog"]] = relationship(back_populates="template")

class MailLog(db.Model):
    __tablename__ = "logs"

    def __init__(self, recipient, timestamp, user_id, template_id):
        self.recipient=recipient
        self.timestamp = timestamp
        self.user_id=user_id
        self.template_id=template_id

    id: Mapped[int] = mapped_column(primary_key=True)
    recipient: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="logs")

    template_id: Mapped[int] = mapped_column(ForeignKey("templates.id"))
    template: Mapped["MailTemplate"] = relationship(back_populates="logs")

class MailSettings(db.Model):
    __tablename__ = "mail_settings"

    def __init__(self, smtp_server, smtp_port, use_tls, email_address, email_password, user_id):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.use_tls = use_tls
        self.email_address = email_address
        self.email_password = email_password
        self.user_id = user_id

    id: Mapped[int] = mapped_column(primary_key=True)    
    smtp_server: Mapped[str] = mapped_column(nullable=False)
    smtp_port: Mapped[int] = mapped_column(nullable=False)
    use_tls: Mapped[bool] = mapped_column(default=True)
    email_address: Mapped[str] = mapped_column(nullable=False)
    email_password: Mapped[str] = mapped_column(nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="mail_settings")