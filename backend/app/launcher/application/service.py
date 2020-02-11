"Application Service"

from typing import List

from ..user.model import User
from .model import Application


def get_all_applications_for_user(user: User) -> List[Application]:
    """Get all applications that a user is authorized to use

    Args:
        user (UserInterface): user to get apps for
    
    Returns:
        List[ApplicationInterface]: list of applications the user is authorized to use
    """

    apps: List[Application] = Application.query.all()

    app_roles = [role.name.split(".")[0] for role in user.roles]

    return [app for app in apps if app.code_name in app_roles]

