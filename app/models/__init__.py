# To avoid circular dependencies, models are imported here
from .user import User
from .message import Message

__all__ = ["Message", "User"]
