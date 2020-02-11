""" Client Schema """

from marshmallow import Schema, fields


class ClientSchema(Schema):
    """ Client Schema """

    id = fields.Integer()
    token = fields.String()
    offering = fields.String()
    name = fields.String()
    description = fields.String()
    logoUrl = fields.String(attribute="logo_url")
    theme = fields.String()
    isActive = fields.Boolean(attribute="is_active")
    createdDatetime = fields.DateTime(attribute="created_datetime")
