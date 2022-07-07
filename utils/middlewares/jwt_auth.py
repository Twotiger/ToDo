from typing import Optional
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from business.user.user_factory import UserFactory
from business.user.user import User
import threading

def need_check(path: str) -> bool:
    """此路径需要进行jwt认证"""
    return path not in ('/api/login')


class JwtAuth:
    _user = {}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if need_check(request.path):

            token = request.META.get("HTTP_AUTHORIZATION")
            if not token:
                return JsonResponse({"errMsg": "权限拒绝!"}, status=401)

            try:
                map = jwt.decode(token, settings.SECRET_KEY,
                                 algorithms=["HS256"])
            except jwt.exceptions.DecodeError:
                return JsonResponse({"errMsg": "权限拒绝!!"}, status=401)

            user_id = map.get("id")
            user =  User(user_id)
            request.god = user
            UserFactory.set(user)


        response = self.get_response(request)

        self.del_user()
        return response


    @classmethod
    def set_user(cls, user):
        cls._user[threading.current_thread()] = user

    @classmethod
    def del_user(cls):
        cls._user.pop(threading.current_thread(), None)

    @classmethod
    def get_request(cls, default=None) -> Optional[User]:
        return cls._user.get(threading.current_thread(), default)