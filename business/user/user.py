from business.task_list.task_list_repository import TaskListRepository
from business.task_list.task_list_factory import TaskListFactory
from business.task.task_repository import TaskRepository
from business.task.task_factory import TaskFactory
from db.models import Account
from django.db.models import F


class User:

    __slots__ = ('id',)

    def __init__(self, id=None):
        self.id = id

    @property
    def task_list_factory(self):
        return TaskListFactory(self)

    @property
    def task_list_repository(self):
        return TaskListRepository(self)

    @property
    def task_repository(self):
        return TaskRepository(self)

    @property
    def task_factory(self):
        return TaskFactory(self)

    def increment_my_day_count(self):
        Account.objects.filter(id=self.id).update(my_day_count=F(
            'my_day_count') + 1)

    def increment_important_count(self):
        Account.objects.filter(id=self.id).update(important_count=F(
            'important_count') + 1)

    def increment_task_count(self):
        Account.objects.filter(id=self.id).update(task_count=F(
            'task_count') + 1)

    def decrement_my_day_count(self):
        Account.objects.filter(id=self.id).update(my_day_count=F(
            'my_day_count') - 1)

    def decrement_important_count(self):
        Account.objects.filter(id=self.id).update(important_count=F(
            'important_count') - 1)
    
    def decrement_task_count(self):
        Account.objects.filter(id=self.id).update(task_count=F(
            'task_count') - 1)

    def get_task_count(self):
        user = Account.objects.get(id=self.id)
        return {"my_day": user.my_day_count, "important": user.important_count, "task": user.task_count}
