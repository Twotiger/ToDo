from pytz import utc
from datetime import timezone
import json
from config import SECRET_KEY
import jwt
import asyncio
import datetime
import logging
import websockets
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger

import threading


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    )

jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite3')
}
executors = {
    'default': {'type': 'threadpool', 'max_workers': 20},
    'processpool': ProcessPoolExecutor(max_workers=5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}


scheduler = AsyncIOScheduler()

# scheduler.configure(jobstores=jobstores, executors=executors,
#                     job_defaults=job_defaults, timezone=utc)
scheduler.configure(executors=executors,
                    job_defaults=job_defaults, timezone=utc)

scheduler.start()

websocket_dict = {}  # user: websocket


async def login(websocket):

    while True:
        data = await websocket.recv()
        json_data = json.loads(data)
        token = json_data.get("token")
        map = jwt.decode(token, SECRET_KEY,
                         algorithms=["HS256"])
        user_id = map.get("id")
        await websocket.send(json.dumps({"type": "msg", "data": "login success"}))

        websocket_dict[user_id] = websocket


def notice(user_id, task_name):
    """将消息发送给指定用户"""
    asyncio.set_event_loop(loop)
    logging.info("websocket_dict = %s", websocket_dict)
    websocket = websocket_dict.get(user_id)
    if not websocket:
        return
    loop.create_task(websocket.send(json.dumps(
        {"user_id": user_id, "type": "notification", "task_name": task_name})))


async def add_notice(websocket):
    """
    接受web端传递过来的消息,验证后添加任务
    """
    recv_text = await websocket.recv()
    json_data = json.loads(recv_text)
    token = json_data["token"]
    map = jwt.decode(token, SECRET_KEY,
                     algorithms=["HS256"])
    user_id = map.get("id")

    repeat = json_data["repeat"]  # class

    date = datetime.datetime.utcfromtimestamp(json_data["notice"])
    interval_type = repeat.get('intervalType', '')
    if interval_type == '':
        s = scheduler.add_job(notice, 'date', run_date=date, args=(
            user_id, json_data["task_name"]), id=str(json_data['task_id']))

    else:
        kwargs = get_kwargs(interval_type, json_data)
        s = scheduler.add_job(notice, **kwargs, args=(
            user_id, json_data["task_name"]))

    logging.info("添加任务 %s, %s", s.id, json_data["task_name"])
    logging.info("下一次提醒: %s", s.next_run_time)


def get_kwargs(interval_type, json_data, id='id'):
    """
    生成定时参数
    """
    date = datetime.datetime.utcfromtimestamp(json_data["notice"])
    res = {}

    # interval = 1
    # if 'repeat' in json_data:
    # interval = json_data["repeat"]['interval']

    if interval_type == '':
        res = dict(trigger='date', run_date=date)
    elif interval_type == 'Daily':
        res = dict(trigger=CronTrigger(
            hour=date.hour, minute=date.minute, second=date.second, timezone=timezone.utc))

    elif interval_type == 'WeekDays':
        res = dict(trigger=CronTrigger(day_of_week="0-4", hour=date.hour,
                   minute=date.minute, second=date.second, start_date=date))

    elif interval_type == 'Weekly':
        day_of_week = f"{date.weekday()}"
        res = dict(trigger=CronTrigger(day_of_week=day_of_week, hour=date.hour,
                   minute=date.minute, second=date.second, start_date=date))

    elif interval_type == 'Monthly':
        res = dict(trigger=CronTrigger(day=date.day, hour=date.hour,
                   minute=date.minute, second=date.second, start_date=date))

    elif interval_type == 'Yearly':
        res = dict(trigger=CronTrigger(month=date.month, day=date.day,
                   hour=date.hour, minute=date.minute, second=date.second, start_date=date))

    res[id] = str(json_data['task_id'])
    return res


async def del_notice(websocket):
    """
    删除任务
    """
    recv_text = await websocket.recv()
    json_data = json.loads(recv_text)
    token = json_data["token"]
    map = jwt.decode(token, SECRET_KEY,
                     algorithms=["HS256"])
    task_id = str(json_data['task_id'])
    scheduler.remove_job(task_id)
    logging.info("删除任务:%s", task_id)


async def modify_notice(websocket):
    """
    修改任务
    """
    recv_text = await websocket.recv()
    json_data = json.loads(recv_text)
    token = json_data["token"]
    map = jwt.decode(token, SECRET_KEY,
                     algorithms=["HS256"])
    task_id = str(json_data['task_id'])
    repeat = json_data["repeat"]
    interval_type = repeat.get('intervalType', '')

    kwargs = get_kwargs(interval_type, json_data, id="job_id")
    task = scheduler.reschedule_job(**kwargs)
    logging.info("修改任务 %s", task_id)
    logging.info("下一次提醒: %s", task.next_run_time)


async def main(websocket, path):

    if path == "/add_notice":
        await add_notice(websocket)
    elif path == '/del_notice':
        await del_notice(websocket)
    elif path == '/modify_notice':
        await modify_notice(websocket)
    else:
        try:
            await login(websocket)
        except Exception as e:
            delete_keys = []
            for key, value in websocket_dict.items():
                if value == websocket:
                    delete_keys.append(key)

            for key in delete_keys:
                del websocket_dict[key]


start_server = websockets.serve(main, '127.0.0.1', 8765)


try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_forever()
except (KeyboardInterrupt, SystemExit):
    pass
