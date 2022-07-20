import json
from datetime import datetime
from typing import List, Union
from utils.business_model import Service
from .task import Task
from db.models import DEFAULT_DATE, DEFAULT_REPEAT



class TaskFactory(Service):

    @classmethod
    def create(cls, data: dict):
        """
        创建Task类
        """
        task = Task()
        if data["deadline"]:
            task.deadline = data["deadline"]
        else:
            task.deadline = DEFAULT_DATE

        if data["repeat"]:
            task.repeat = data["repeat"]
        else:
            task.repeat = DEFAULT_REPEAT

        if data["notice"]:
            task.notice = data["notice"]
        else:
            task.notice = DEFAULT_DATE

        # 对重复任务，添加deadline
        if task.repeat['intervalType'] and task.deadline == DEFAULT_DATE:
            task.deadline = datetime.now()

        task.is_my_day = data.get("is_my_day", False)
        task.is_important = data.get("is_important", False)
        task.task_list_id = data.get("task_list_id",  0)

        task.name = data["name"]
        return task
