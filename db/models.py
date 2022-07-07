
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from pytz import timezone


default = 0
finished = 1


class Account(AbstractUser):
    my_day_count = models.IntegerField(default=0)
    important_count = models.IntegerField(default=0)
    task_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'auth_user'


class TaskList(models.Model):
    """任务列表"""
    user_id = models.BigIntegerField()
    parent_id = models.BigIntegerField(default=0)  # 如果不为0,是子列表
    task_type = models.IntegerField()  # 2:group | 1:list
    count = models.IntegerField(default=0)  # 任务数量
    name = models.CharField(max_length=100)
    index = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "task_list"


DEFAULT_DATE = datetime.datetime(
    1, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)


class Task(models.Model):

    name = models.CharField(max_length=100)
    is_my_day = models.BooleanField(default=False)
    is_important = models.BooleanField(default=False)
    deadline = models.DateTimeField(default=DEFAULT_DATE)
    notice = models.DateTimeField(default=DEFAULT_DATE)
    repeat = models.CharField(max_length=200)

    status = models.BooleanField(default=False)
    remark = models.TextField()

    user_id = models.BigIntegerField(default=0)
    task_list_id = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(default=DEFAULT_DATE)

    class Meta:
        db_table = "task"
