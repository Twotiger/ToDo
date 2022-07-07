from typing import List
from utils.business_model import Service
from .task_list import TaskList, TaskGroup
from db.models import Task, TaskList as TaskListDB


class TaskListFactory(Service):

    @classmethod
    def create(cls, data: dict):
        if data["task_type"] == "list":
            model = TaskList()
            model.name = data["name"]
            model.parent_id = data.get("parent_id", 0)
        else:
            model = TaskGroup()
            model.name = data["name"]
        return model
