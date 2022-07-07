from typing import List, Union
from utils.business_model import Service
from .task import Task
from db.models import DEFAULT_DATE


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
            task.repeat = ''

        if data["notice"]:
            task.notice = data["notice"]
        else:
            task.notice = DEFAULT_DATE

        task.is_my_day = data.get("is_my_day", False)
        task.is_important = data.get("is_important", False)
        task.task_list_id = data.get("task_list_id",  0)

        task.name = data["name"]
        return task
