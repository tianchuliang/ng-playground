"""Role interface"""

from datetime import datetime

from mypy_extensions import TypedDict


class RoleInterface(TypedDict, total=False):
    """Role Interface"""

    id: int
    name: str
    description: str
    created_by: str
    last_updated_by: str
    created_datetime: datetime
    last_updated_datetime: datetime
