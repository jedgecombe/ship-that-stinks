import logging

from flask import current_app, Flask, redirect, url_for

from ship_that_stinks.database.table_definitions import *
from ship_that_stinks.database.create import create_database, init_app


def create_app(config, debug=False, testing=False, config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(config)

    app.debug = debug
    app.testing = testing

    if config_overrides:
        app.config.update(config_overrides)

    # Configure logging
    if not app.testing:
        logging.basicConfig(level=logging.INFO)

    # Setup the data model.
    with app.app_context():
        init_app(app)

    # Register the Bookshelf CRUD blueprint.
    from .crud import crud

    app.register_blueprint(crud, url_prefix="/participants")

    # Add a default root route.
    @app.route("/")
    def index():
        return redirect(url_for("crud.list"))

    # Add an error handler. This is useful for debugging the live application,
    # however, you should disable the output of the exception for production
    # applications.
    @app.errorhandler(500)
    def server_error(e):
        return (
            """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(
                e
            ),
            500,
        )

    return app
