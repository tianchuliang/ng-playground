""" Application Model """

from sqlalchemy.sql import func

from app import db


class Application(db.Model):  # type: ignore
    """Application Table"""

    __tablename__ = "application_t"
    __table_args__ = {"schema": "common"}

    application_id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    code_name = db.Column(db.String(10), unique=True)
    description = db.Column(db.String(255))
    app_url = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    icon_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    created_by = db.Column(db.String(255), nullable=False, server_default="admin")
    last_updated_by = db.Column(db.String(255), nullable=False, server_default="admin")
    created_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now()
    )
    last_updated_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<Application '{}'>".format(self.name)
