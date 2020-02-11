""" Application Schema """
from marshmallow import Schema, fields


class ApplicationSchema(Schema):
    """ Application Schema """

    applicationId = fields.Integer(attribute="application_id")
    name = fields.String(required=True)
    description = fields.String(required=True)
    codeName = fields.String(required=True, attribute="code_name")
    imageUrl = fields.String(required=True, attribute="image_url")
    iconUrl = fields.String(required=True, attribute="icon_url")
    isActive = fields.Boolean(attribute="is_active")
    createdDatetime = fields.DateTime(attribute="created_datetime")
