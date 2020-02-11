"""Application interface"""

from datetime import datetime

from mypy_extensions import TypedDict


class ApplicationInterface(TypedDict, total=False):
    """Application Interface"""

    application_id: int
    name: str
    code_name: str
    description: str
    app_url: str
    image_url: str
    is_active: bool
    created_by: str
    last_updated_by: str
    created_datetime: datetime
    last_updated_datetime: datetime
