"Role Model"

from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app import db
from app.shared import PsqlCoeMixin


class Client(PsqlCoeMixin, db.Model):  # type: ignore
    """Client Table"""

    __tablename__ = "client_t"
    __table_args__ = {"schema": "common"}

    id = db.Column(db.String(255), primary_key=True)
    token = db.Column(UUID(as_uuid=True), unique=True, default=uuid4)

    # Standard OR Pro Offering
    offering = db.Column(db.String(80), server_default="standard")
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    logo_url = db.Column(db.String(255))
    theme = db.Column(db.String(255), server_default="default")
    is_active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(255), nullable=False, server_default="admin")
    last_updated_by = db.Column(db.String(255), nullable=False, server_default="admin")
    created_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now()
    )
    last_updated_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()
    )
    users = db.relationship("User", backref="client", lazy=True)

    def __repr__(self):
        return "<Client '{}'>".format(self.name)
