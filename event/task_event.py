import websockets
import asyncio
import json
import jwt
from todo.settings import SECRET_KEY
from db.models import Task as TaskDB, DEFAULT_DATE
from business.user.user_factory import UserFactory


def get_token():

    user = UserFactory.get()

    token_dict = {
        "id": user.id,
    }
    jwt_token = jwt.encode(
        token_dict, SECRET_KEY, algorithm="HS256"
    )
    return jwt_token


async def send_add_notice(task):
    async with websockets.connect(
            'ws://localhost:8765/add_notice') as websocket:
        await websocket.send(json.dumps({"token": get_token(),
                                         "task_name": task.name,
                                         "task_id": task.id,
                                         "repeat": task.repeat,
                                         "notice": task.notice.timestamp()})
                             )


async def send_del_notice(task_id, task_name):
    async with websockets.connect(
            'ws://localhost:8765/del_notice') as websocket:
        await websocket.send(json.dumps({"token": get_token(), "task_name": task_name, "task_id": task_id}))


async def send_modify_notice(task):
    async with websockets.connect(
            'ws://localhost:8765/modify_notice') as websocket:
        await websocket.send(json.dumps({"token": get_token(), "task_name": task.name, "task_id": task.id, "repeat": task.repeat, "notice": task.notice.timestamp()}))


class TaskEvent:

    @classmethod
    def add_notice_job(cls, task):
        if not task.notice:
            return
        if task.notice == DEFAULT_DATE:
            return
        loop = asyncio.new_event_loop()
        rv = loop.run_until_complete(send_add_notice(task))
        return rv

    @classmethod
    def del_notice_job(cls, task):
        if not task.notice:
            return
        loop = asyncio.new_event_loop()
        rv = loop.run_until_complete(send_del_notice(task.id, task.name))
        return rv

    @classmethod
    def modify_notice_job(cls, task):
        loop = asyncio.new_event_loop()
        rv = loop.run_until_complete(send_modify_notice(task))
        return rv
