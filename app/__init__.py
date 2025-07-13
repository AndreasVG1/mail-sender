from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config.from_pyfile("../config.py", silent=True)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register routes or blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app