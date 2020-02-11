"User Controller"
from flask import abort
from flask_accepts import responds
from flask_praetorian import auth_required, current_user, roles_required
from flask_restplus import Namespace, Resource

from .model import Client
from .schema import ClientSchema

api = Namespace("Client", description="Client Resources")


@api.route("")
@api.doc(security="jwt")
class ClientIdResourceNamespace(Resource):
    """ Client resource. """

    @responds(schema=ClientSchema, api=api)
    @auth_required
    def get(self):
        """ Get method for client resource. """
        user = current_user()

        client = Client.query.get(str(user.client_id))
        if not client:
            abort(404, "Client was not found")

        return client


@api.route("/all")
@api.doc(security="jwt")
class ClientResourceFlaskAccepts(Resource):
    """ Client resource. """

    @responds(schema=ClientSchema(many=True), api=api)
    @roles_required("admin")
    def get(self):
        """ Get method for client resource. """
        users = Client.query.all()

        return users
