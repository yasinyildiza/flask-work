"""A basic Flask application yielding user register/login/logout."""

from flask import Flask
from .blueprints import category, tag, user, usertracking
from .models import db

# configuration
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

# Flask-SQLAlchemy configuration
SQLALCHEMY_DATABASE_URI = 'sqlite:///mywallet.db'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True


def create_app():
    """initialize Flask app"""

    # create application
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config.from_envvar('MYWALLET_SETTINGS')

    # init database
    db.init_app(app)

    # register bluprints
    app.register_blueprint(category.bp, url_prefix='/category')
    app.register_blueprint(tag.bp, url_prefix='/tag')
    app.register_blueprint(usertracking.bp, url_prefix='/usertracking')
    app.register_blueprint(user.bp, url_prefix='/user')

    return app
