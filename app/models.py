from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey, DateTime
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    templates: Mapped[list["MailTemplate"]] = relationship(back_populates="users")
    logs: Mapped[list["MailLog"]] = relationship(back_populates="users")

class MailTemplate(db.Model):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content_html: Mapped[str] = mapped_column(Text, nullable=False)
    file_path: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="templates")
    logs: Mapped[list["MailLog"]] = relationship(back_populates="templates")

class MailLog(db.Model):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipient: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="logs")

    template_id: Mapped[int] = mapped_column(ForeignKey("templates.id"))
    template: Mapped["MailTemplate"] = relationship(back_populates="logs")