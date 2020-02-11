""" User Controller """
from flask import abort
from flask_accepts import responds
from flask_praetorian import roles_required
from flask_restplus import Namespace, Resource

from .model import User
from .schema import UserSchema

api = Namespace("User", description="User Resources")


@api.route("/")
@api.doc(security="jwt")
class UserResourceFlaskAccepts(Resource):
    """ User resource """

    @responds(schema=UserSchema(many=True), api=api)
    @roles_required("admin")
    def get(self):
        """ Get method for user entity. """
        users = User.query.all()

        return users


@api.route("/<string:user_id>")
@api.doc(security="jwt")
class UserIdResourceNamespace(Resource):
    """ User resource """

    @responds(schema=UserSchema, api=api)
    @roles_required("admin")
    def get(self, user_id: str):
        """ Get method for user entity. """

        user = User.query.get(user_id)
        if not user:
            abort(404, "User was not found")

        return user
