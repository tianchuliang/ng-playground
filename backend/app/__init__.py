"Main Flask App"
import ntpath
from logging import Logger
from typing import List

from flask import Flask, abort, jsonify, request
from flask.helpers import send_from_directory
from flask_accepts import accepts, responds

# Flask Admin for CRUD
from flask_admin import Admin
from flask_admin import helpers as admin_helpers
from flask_admin.contrib.sqla import ModelView
from flask_caching import Cache
from flask_cors import CORS
from flask_executor import Executor
from flask_migrate import Migrate
from flask_praetorian import Praetorian, auth_required, roles_required
from flask_restplus import Api, Namespace, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound

# from werkzeug.middleware.profiler import ProfilerMiddleware


db = SQLAlchemy()
guard = Praetorian()
executor = Executor()
cache = Cache()


def create_app(config_name: str) -> Flask:
    """Create the Flask application

    Args:
        config_name (str): Config name mapping to Config Class

    Returns:
        [Flask]: Flask Application
    """
    # pylint: disable=import-outside-toplevel

    from app.config import config_by_name
    from app.launcher.client.model import Client
    from app.launcher.user.model import User
    from app.launcher.application.model import Application
    from app.launcher.role.model import Role
    from app.launcher import MetaView, UserView
    from app.routes import register_routes

    # Create the app
    app = Flask(__name__)

    # Set CORS
    CORS(app, resources={"*": {"origins": "*"}})

    # Log the current config name being used and setup app with the config
    app.logger.debug(f"CONFIG NAME: {config_name}")
    config = config_by_name[config_name]
    app.config.from_object(config)

    # Middleware to create .prof files. DEBUG ONLY
    # app.wsgi_app = ProfilerMiddleware(
    #     app.wsgi_app, profile_dir="/Users/dasaf/Desktop/profile"
    # )

    cache.init_app(app)

    # Setup Flask Executor
    executor.init_app(app)

    # Setup Flask Admin
    admin = Admin(app, name="Admin Console", template_mode="bootstrap3")
    admin.add_view(UserView(User, db.session))
    admin.add_view(MetaView(Role, db.session))
    admin.add_view(MetaView(Client, db.session))
    admin.add_view(MetaView(Application, db.session))

    # Initialize the database
    db.init_app(app)

    # Initialize flask migrate alembic
    migrate = Migrate(app, db)  # pylint: disable=unused-variable

    # Initialize Rest+ API
    register_routes(app, "/api")

    # Initialize the flask-praetorian instance for the app
    guard.init_app(app, User)

    # Setup Static Rule
    @app.route("/", defaults={"file": ""})
    @app.route("/<path:file>")
    def serve_static(file):  # pylint: disable=unused-variable
        """ Deliver all static content on a specified url. """

        try:
            return send_from_directory(config.STATIC_FOLDER, file)
        except NotFound:
            if "." in ntpath.basename(file):
                abort(404)
            else:
                return send_from_directory(config.STATIC_FOLDER, "index.html")

    return app