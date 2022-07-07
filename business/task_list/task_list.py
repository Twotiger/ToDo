import json

from django.db.models import F

from utils.business_model import Model
from utils.datetime import get_next_deadline
from business.task.task import Task
from business.user.user_factory import UserFactory
from db.models import TaskList as TaskListDB, Task as TaskDB
from event.task_event import TaskEvent


class BaseTaskList(Model):
    """
    任务列表
    """
    __slots__ = ("name", "task_type")


class TaskList(BaseTaskList):

    __slots__ = ("name", "id", "task_type", "user_id",
                 "parent_id", "index", "count")

    def __init__(self, db_model=None):
        super().__init__(db_model)
        self.task_type = "list"

    def add_task(self, task: Task):
        user = UserFactory.get()
        user.task_repository.add(task)
        # task list 自增
        self.increment_task_count(task)

    def increment_task_count(self, task: Task):
        user = UserFactory.get()
        if task.is_my_day:
            user.increment_my_day_count()
        if task.is_important:
            user.increment_important_count()
        if self.id == 0:
            user.increment_task_count()
        else:
            TaskListDB.objects.filter(id=self.id).update(count=F("count") + 1)

    def decrement_task_count(self, task: Task):
        user = UserFactory.get()
        if task.is_my_day:
            user.decrement_my_day_count()
        if task.is_important:
            user.decrement_important_count()
        if self.id == 0:
            user.decrement_task_count()
        else:
            TaskListDB.objects.filter(id=self.id).update(count=F("count") - 1)

    def complete_task(self, task: Task):
        task.complete()
        TaskEvent.del_notice_job(task)
        if task.repeat:
            deadline = get_next_deadline(task.deadline, task.repeat)
            model = TaskDB(name=task.name,
                           repeat=json.dumps(task.repeat),
                           remark=task.remark,
                           user_id=task.user_id,
                           is_important=task.is_important,
                           deadline=deadline)
            model.save()
            user = UserFactory.get()
            new_task = user.task_repository.get_by_id(model.id)
            TaskEvent.add_notice_job(new_task)

        else:
            self.decrement_task_count(task)

    def uncomplete_task(self, task: Task):
        task.uncomplete()
        self.increment_task_count(task)

    def delete_task(self, task):
        user = UserFactory.get()
        TaskEvent.del_notice_job(task)
        self.decrement_task_count(task)
        TaskDB.objects.filter(id=task.id, user_id=user.id).delete()


class TaskGroup(BaseTaskList):
    __slots__ = ("name", "id", "task_type", "index", "user_id", "parent_id")

    def __init__(self, db_model=None):
        super().__init__(db_model)
        self.task_type = "group"
