import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy



logger = logging.getLogger(__name__)

db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    db.init_app(app)


def create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    from ship_that_stinks.database.table_definitions import *

    app = Flask(__name__)
    app.config.from_pyfile("../../config.py")
    init_app(app)
    with app.app_context():
        db.create_all()
    logger.info("Database setup")


if __name__ == "__main__":
    create_database()
