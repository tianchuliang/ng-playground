""" Launcher Barrel """
from flask import Blueprint, abort
from flask_admin.contrib.sqla import ModelView
from flask_praetorian import PraetorianError, current_user
from flask_restplus import Api, Namespace
from wtforms.fields import PasswordField

from app import guard

API_NAME = "launcher"

def register_routes(app, root="/api"):
    """ Register routes for market price explorer. """
    # pylint: disable= import-outside-toplevel
    from .application.controller import api as application_api
    from .auth.controller import api as auth_api
    from .client.controller import api as client_api
    from .user.controller import api as user_api

    blueprint = Blueprint(API_NAME, __name__)

    api = Api(
        blueprint,
        title="Launch Dock API",
        version="0.1.0",
        prefix="",
        doc="/docs",
        authorizations={
            "jwt": {"type": "apiKey", "in": "header", "name": "Authorization"}
        },
    )

    PraetorianError.register_error_handler_with_flask_restplus(api)

    api.add_namespace(user_api, path="/user")
    api.add_namespace(auth_api, path="/auth")
    api.add_namespace(application_api, path="/application")
    api.add_namespace(client_api, path="/client")
    app.register_blueprint(blueprint, url_prefix=f"{root}/{API_NAME}")

    return app


class MetaView(ModelView):
    """ MetaView model view for flask admin. """

    can_delete = False
    can_export = True
    create_modal = True
    edit_modal = True

    form_excluded_columns = ["created_datetime"]


class UserView(MetaView):
    """ UserView meta view for flask admin. """

    column_exclude_list = ["password"]
    form_excluded_columns = [
        "password",
        "created_datetime",
        "last_login_datetime",
        "last_login_ip",
    ]
    column_searchable_list = ["email"]

    # On the form for creating or editing a User, don't display a field corresponding
    # to the model's password field. There are two reasons for this. First, we want to
    # encrypt the password before storing in the database. Second, we want to use a
    # password field (with the input masked) rather than a regular text field.
    def scaffold_form(self):

        # Start with the standard form as provided by Flask-Admin. We've already told
        # Flask-Admin to exclude the password field from this form.
        form_class = super(UserView, self).scaffold_form()

        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField("Change Password")
        return form_class

    # This callback executes when the user saves changes to a newly-created or edited
    # User -- before the changes are committed to the database.
    def on_model_change(self, form, model, is_created):

        # If the password field isn't blank...
        if len(model.password2) > 0:

            # ... then encrypt the new password prior to storing it in the database. If
            # the password field is blank, the existing password in the database will be
            # retained.
            model.password = guard.hash_password(model.password2)
