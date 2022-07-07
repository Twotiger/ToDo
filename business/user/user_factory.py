from typing import TYPE_CHECKING, Optional
import threading

if TYPE_CHECKING:
    from business.user import user


class UserFactory():

    _user = {}

    @classmethod
    def set(cls, user):
        cls._user[threading.current_thread()] = user

    @classmethod
    def get(cls, default=None) -> Optional["user.User"]:
        return cls._user.get(threading.current_thread(), default)
