import time

import jwt
from django.views import View
from db.models import Account as AccountDB
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate

from todo.settings import SECRET_KEY, SALT
from utils.password import gener_password


class Account(View):
    """账号
    """

    def get(self, request):

        user = request.god
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
        return JsonResponse(data)


@require_http_methods(["POST"])
def login(request):
    data = request.json

    user = authenticate(username=data["username"], password=data["password"])

    if user is None:
        return JsonResponse({"errMsg": "用户名或密码错误"}, status=401)

    token_dict = {
        "id": user.id,
        "username": user.username,
        "t": time.time(),
    }
    headers = {"alg": "HS256", "typ": "JWT"}
    jwt_token = jwt.encode(
        token_dict, SECRET_KEY, algorithm="HS256", headers=headers
    )
    return JsonResponse({"errMsg": "", "token": jwt_token})
