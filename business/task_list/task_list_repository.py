from typing import List, Union
from utils.business_model import Service
from .task_list import TaskList, TaskGroup
from db.models import  TaskList as TaskListDB


class TaskListRepository(Service):

    def add_task_list(self, task_list: Union[TaskList, TaskGroup]) -> int:
        """
        添加
        """
        last = TaskListDB.objects.filter(
            user_id=self.parent.id).order_by("-index").first()
        
        index = 1
        if last:
            index = last.index + 1
        if task_list.task_type == "list":
            mode = TaskListDB(name=task_list.name, task_type=1, user_id=self.parent.id, index=index)
        else:
            mode = TaskListDB(name=task_list.name, task_type=2, user_id=self.parent.id, index=index)
        mode.save()
        return mode.id


    def filter(self) -> List:
        models = TaskListDB.objects.filter(
            user_id=self.parent.id).order_by( "parent_id","index")
        data = []
        for model in models:
            if model.task_type == 1:
                data.append(TaskList(model))
            else:
                data.append(TaskGroup(model))
        return data

    def get_by_id(self, task_list_id: int):
        if task_list_id == 0:
            task_list = TaskList()
            task_list.id = 0
            task_list.name = "任务"
            return task_list

        model = TaskListDB.objects.filter(
            id=task_list_id, user_id=self.parent.id).first()
        if model:
            if model.task_type == 1:
                return TaskList(model)
            else:
                return TaskGroup(model)
