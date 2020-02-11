""" Auth API Schema """
import re

from marshmallow import Schema, ValidationError, fields
from flask import current_app
from app.launcher.user.schema import UserSchema


def must_not_be_blank(data: str):
    """ Test if a parameter is blank. """
    if not data:
        raise ValidationError("Blank Input.")


def password_policy(password: str):
    """Password Policy for hat-trick application
    
    Args:
        password (str): password to validate against policy
    
    Raises:
        ValidationError: if password does not meet policy
    """
    pass_pol = re.compile(current_app.config["PASSWORD_POLICY"])
    if not pass_pol.match(password):
        raise ValidationError(
            "Password does not meet the security policy. The password must contain a "
            + "minimum of eight characters, at least one uppercase letter, one "
            + "lowercase letter, one number and one special character."
        )


class ChangePasswordResponseSchema(Schema):
    """ Change Password Response Schema """

    status = fields.Str(attribute="status")
    accessToken = fields.Str(attribute="accessToken")
    message = fields.Str(attribute="message")


class ChangePasswordSchema(Schema):
    """ User schema for password changes. """

    username = fields.Email(required=True, description="Email")
    currentPassword = fields.String(required=True, validate=must_not_be_blank)
    newPassword = fields.String(required=True, validate=password_policy)


class UserLoginResponseSchema(Schema):
    """Response for Successful Login"""

    accessToken = fields.Str(attribute="accessToken")


class UserLoginSchema(Schema):
    """ User schema for login. """

    username = fields.Email(required=True, description="Email")
    password = fields.String(required=True, validate=must_not_be_blank)


class UserSchemaJsonToken(UserSchema):
    """ User schema with json token. """

    isActive = fields.Boolean(attribute="is_active")
    lastPasswordDatetime = fields.DateTime(attribute="last_password_datetime")
    forcePasswordChangeSet = fields.Boolean(attribute="force_password_change")
