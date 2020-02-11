""" Role Schema """
from marshmallow import Schema, fields


class RoleSchema(Schema):
    """ Role Schema """

    roleId = fields.Integer(attribute="role_id")
    name = fields.String(required=True)
    description = fields.String()
