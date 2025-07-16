import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import Config

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    print(app.config["SQLALCHEMY_DATABASE_URI"])
    # Register routes or blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app