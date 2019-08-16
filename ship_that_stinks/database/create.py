import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from ship_that_stinks.app import init_app

logger = logging.getLogger(__name__)

db = SQLAlchemy()


def create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """

    app = Flask(__name__)
    app.config.from_pyfile("../../config.py")
    init_app(app)
    with app.app_context():
        db.create_all()
    logger.info("Database setup")


if __name__ == "__main__":
    from ship_that_stinks.database.table_definitions import *
    create_database()
