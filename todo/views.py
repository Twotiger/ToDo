import os
import base64
from io import BytesIO
import time

import jwt
from aiohttp import web
from todo.verification_code import get_verification_code
from todo.settings import SECRET_KEY

class MyView(web.View):
    async def get(self):
        data = {'some': 'data'}
        return web.json_response(data)

    async def post(self):
        return web.Response(text="Hello, world")


async def verification_code(request):
    image, code = get_verification_code()
    token_dict = {"t": time.time(), "code": code}
    headers = {"alg": "HS256", "typ": "JWT"}
    jwt_token = jwt.encode(
        token_dict, SECRET_KEY, algorithm="HS256", headers=headers
    )
    buffer = BytesIO()
    image.save(buffer, "PNG")
    str_data = buffer.getvalue()
    img = base64.b64encode(str_data)
    return web.json_response({"img": img.decode("utf-8"), "token": jwt_token})
