from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from config import Config
from flask_login import LoginManager

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()


def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)

    # Initialize flask-login
    login_manager.init_app(app)
    login_manager.login_view = "auth.login" # type: ignore

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    with app.app_context():
        from . import models
        db.create_all()

    # Register routes or blueprints
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from.routes.crud import crud as crud_blueprint
    app.register_blueprint(crud_blueprint)

    from.routes.log import log as log_blueprint
    app.register_blueprint(log_blueprint)

    return app