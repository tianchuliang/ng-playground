"Auth Controller"
from datetime import datetime

from flask import abort, request, current_app
from flask_accepts import accepts, responds
from flask_restplus import Namespace, Resource

from app import guard

from ..user.model import PasswordHistory, User
from .schema import (
    ChangePasswordResponseSchema,
    ChangePasswordSchema,
    UserLoginResponseSchema,
    UserLoginSchema,
    UserSchemaJsonToken,
)

api = Namespace("Auth", description="User Resources")


@api.route("/login")
class UserLoginResource(Resource):
    """ User Login Resource. """

    @accepts(schema=UserLoginSchema, api=api)
    @responds(schema=UserLoginResponseSchema)
    def post(self):
        """ Post method for user login. """
        username = request.parsed_obj["username"]
        password = request.parsed_obj["password"]
        max_password_age = current_app.config["MAX_PASSWORD_AGE"]

        user = guard.authenticate(username, password)
        password_age = (datetime.utcnow() - user.last_password_datetime).days

        if user.force_password_change:
            abort(409, "You must change your password to proceed.")
        elif password_age >= max_password_age:
            abort(
                409,
                f"You must change your password to proceed. "
                f"Maximum password age is {max_password_age} "
                f"days. Your password was last updated {password_age} days ago.",
            )
        else:
            ret = {
                "accessToken": guard.encode_jwt_token(
                    user, custom_claims=UserSchemaJsonToken().dump(user)
                )
            }
        return ret


@api.route("/changePassword")
class ChangePasswordResource(Resource):
    """ Password change resource. """

    @accepts(schema=ChangePasswordSchema, api=api)
    @responds(schema=ChangePasswordResponseSchema)
    def post(self):
        """ Post method for changing password. """
        username = request.parsed_obj["username"]
        current_password = request.parsed_obj["currentPassword"]
        new_password = request.parsed_obj["newPassword"]
        password_history_repeat = current_app.config["PASSWORD_HISTORY_REPEAT"]

        password_history = PasswordHistory.get_history(
            username, password_history_repeat
        )
        user = guard.authenticate(username, current_password)

        if current_password == new_password:
            return abort(400, "New password cannot be the same as current password.")

        for old_password in password_history:
            # Using the private method to verify the password history because
            # same password has different hashes and hashes cannot be compared.
            # To use the same context had to use the verify password private method.
            #
            if guard._verify_password(new_password, old_password):
                return abort(
                    400,
                    f"New password cannot be reused from last"
                    f" {password_history_repeat} passwords",
                )

        if not User.update(username, current_password, new_password):
            abort(500, "Change password error. Please contact support")

        user = guard.authenticate(username, new_password)

        return {
            "status": "Success",
            "accessToken": guard.encode_jwt_token(
                user, custom_claims=UserSchemaJsonToken().dump(user)
            ),
            "message": None,
        }
