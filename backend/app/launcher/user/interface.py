"""User interface"""

from datetime import datetime
from typing import List

from mypy_extensions import TypedDict

from app.launcher.role.interface import RoleInterface


class UserInterface(TypedDict, total=False):
    """User Interface"""

    id: int
    client_id: str
    email: str
    password: str

    roles: List[RoleInterface]

    is_active: bool
    force_password_change: bool
    last_login_datetime: datetime
    last_login_ip: str
    last_password_datetime: datetime

    created_by: str
    last_updated_by: str
    created_datetime: datetime
    last_updated_datetime: datetime
