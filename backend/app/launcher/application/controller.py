""" Application API """
from flask import abort
from flask_accepts import responds
from flask_praetorian import auth_required, current_user
from flask_restplus import Namespace, Resource

from .model import Application
from .schema import ApplicationSchema
from .service import get_all_applications_for_user

api = Namespace("Application", description="Application Resources")


@api.route("")
@api.doc(security="jwt")
class ApplicationRootResource(Resource):
    """ Application resource. """

    @responds(schema=ApplicationSchema(many=True), api=api)
    @auth_required
    def get(self):
        """ Get method for application resource. """
        user_apps = get_all_applications_for_user(current_user())

        return user_apps


@api.route("/<int:application_id>")
@api.doc(security="jwt")
class ApplicationIdResource(Resource):
    """ Application resource. """

    @responds(schema=ApplicationSchema, api=api)
    @auth_required
    def get(self, application_id: int):
        """ Get method for application resource. """

        app = Application.query.get(application_id)
        if not app:
            abort(404, "Application was not found")

        return app
