""" User Schema """
from marshmallow import Schema, fields

from app.launcher.role.schema import RoleSchema


class UserSchema(Schema):
    """ User schema. """

    userId = fields.String(attribute="id")
    email = fields.Email(required=True, description="Email")
    clientId = fields.String(attribute="client_id")
    roles = fields.Nested(RoleSchema, many=True)
    isActive = fields.Boolean(attribute="is_active")
    lastLoginIp = fields.String(attribute="last_login_ip")
    createdDatetime = fields.DateTime(attribute="created_datetime")
    lastLoginDatetime = fields.DateTime(attribute="last_login_datetime")


class UserSchemaWithPassword(UserSchema):
    """ User schema with password. """

    password = fields.String(required=True)
