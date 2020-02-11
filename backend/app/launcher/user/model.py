""" User Model. """
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.sql import desc, expression, func

# pylint: disable=no-member
from app import db, guard
from app.launcher.client.model import Client
from app.launcher.role.model import Role


class RolesUsers(db.Model):  # type: ignore
    """ Cross table of roles to users. """

    __tablename__ = "roles_users_t"
    __table_args__ = {"schema": "common"}

    id = db.Column(db.String(), primary_key=True)
    user_id = db.Column("user_id", db.String(), db.ForeignKey("common.user_t.id"))
    role_id = db.Column("role_id", db.String(), db.ForeignKey("common.role_t.id"))
    created_by = db.Column(db.String(255), nullable=False, server_default="admin")
    last_updated_by = db.Column(db.String(255), nullable=False, server_default="admin")
    created_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now()
    )
    last_updated_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()
    )


class User(db.Model):  # type: ignore
    """A generic user model that might be used by an app powered by flask-praetorian"""

    __tablename__ = "user_t"
    __table_args__ = {"schema": "common"}

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    roles = db.relationship(
        Role, secondary="common.roles_users_t", backref=db.backref("users", lazy=True)
    )
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    force_password_change = db.Column(db.Boolean, default=True, server_default="true")
    last_login_datetime = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(30))
    last_password_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now()
    )
    created_by = db.Column(db.String(255), nullable=False, server_default="admin")
    last_updated_by = db.Column(db.String(255), nullable=False, server_default="admin")
    created_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now()
    )
    last_updated_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    client_id = db.Column(
        db.String(255), db.ForeignKey(f"{Client.get_table_name()}.id"), nullable=False
    )

    @property
    def rolenames(self):
        """ Get all the role names for the user. """
        try:
            return [role.name for role in self.roles]
        except Exception:  # pylint: disable=broad-except
            return []

    @classmethod
    def lookup(cls, email: str):
        """ Lookup a user by email. """
        return cls.query.filter(
            func.lower(cls.email) == func.lower(email)
        ).one_or_none()

    @classmethod
    def identify(cls, user_id: int):
        """ Get the identifier for a given user. """
        return cls.query.get(user_id)

    @property
    def identity(self):
        """ Get the identifier for this user. """
        return self.id

    def is_valid(self):
        return self.is_active

    @classmethod
    def update(cls, email: str, currentpassword: str, newpassword: str):
        """ Update Password. """
        usr = guard.authenticate(email, currentpassword)
        usr.password = guard.hash_password(newpassword)
        usr.last_password_datetime = datetime.utcnow()
        usr.force_password_change = expression.false()
        db.session.commit()
        PasswordHistory.add(usr.id, guard.hash_password(currentpassword))
        return True

    def __repr__(self):
        return f"<User {self.id} - {self.email}>"


class PasswordHistory(db.Model):  # type: ignore
    """ Password History table to users. """

    __tablename__ = "password_history_t"
    __table_args__ = {"schema": "common"}

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column("user_id", db.String(), db.ForeignKey("common.user_t.id"))
    password = db.Column(db.String(255))
    created_by = db.Column(db.String(255), nullable=False, server_default="admin")
    last_updated_by = db.Column(db.String(255), nullable=False, server_default="admin")
    created_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now()
    )
    last_updated_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    @classmethod
    def add(cls, user_id: int, password: str):
        """ Add Password History. """
        history = PasswordHistory(user_id=user_id, password=password)
        db.session.add(history)
        db.session.commit()
        return True

    @classmethod
    def get_history(cls, username: str, count: int = 5):
        """ Get Password History.
            Default coount is set to 4 for last 5 password to include current password
            and the last 4 password from the history
        """
        usr = User.lookup(username)
        limit_count = count - 1
        history = (
            cls.query.filter_by(user_id=usr.id)
            .order_by(desc(PasswordHistory.created_datetime))
            .limit(limit_count)
            .all()
        )
        return [ph.password for ph in history]
