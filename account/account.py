import time

import jwt
from django.views import View
# from django.contrib.auth.models import User
from db.models import Account as AccountDB
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate

from todo.settings import SECRET_KEY, SALT
from utils.password import gener_password


class Account(View):
    """账号
    """
    async def get(self):
        data = {'some': 'data'}
        return web.json_response(data)

    async def post(self):
        """新建"""
        return web.Response(text="Hello, world")

    async def put(self):
        """"""
        return web.Response(text="Hello, world")

@require_http_methods(["POST"])
def login(request):
    data = request.json


    # user = AccountDB.objects.filter(username=data["username"], password=data["password"]).first()
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
