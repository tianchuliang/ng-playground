"Role Model"

from sqlalchemy.sql import func

from app import db

ADMIN = "admin"

CC_PRO_ROLE = "cc.pro"
CC_STD_ROLE = "cc.std"

MPE_PRO_ROLE = "mpe.pro"
MPE_STD_ROLE = "mpe.std"

PE_PRO_ROLE = "pe.pro"
PE_STD_ROLE = "pe.std"


class Role(db.Model):  # type: ignore
    """Role Table"""

    __tablename__ = "role_t"
    __table_args__ = {"schema": "common"}

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    created_by = db.Column(db.String(255), nullable=False, server_default="admin")
    last_updated_by = db.Column(db.String(255), nullable=False, server_default="admin")
    created_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now()
    )
    last_updated_datetime = db.Column(
        db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return "<Role '{}'>".format(self.name)
