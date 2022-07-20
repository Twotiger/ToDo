from typing import List, Union
import json
from datetime import datetime

from django.db.models import Q
from utils.business_model import Service
from .task import Task
from db.models import Task as TaskDB, DEFAULT_DATE
from event.task_event import TaskEvent


class TaskRepository(Service):

    def add(self, model: Task):

        m = TaskDB(name=model.name,
                   deadline=model.deadline,
                   notice=model.notice,
                   repeat=json.dumps(model.repeat),
                   is_my_day=model.is_my_day,
                   is_important=model.is_important,
                   task_list_id=model.task_list_id,
                   user_id=self.parent.id)
        m.save()

        new_model = self.get_by_id(m.id)
        TaskEvent.add_notice_job(new_model)
        return m.id

    def get_by_id(self, task_id: int):
        task = TaskDB.objects.filter(
            id=task_id, user_id=self.parent.id).first()
        if task:
            return Task(task)
        return None

    def filter(self, data):
        if "is_my_day" in data:
            now = datetime.now()
            start_date = datetime(now.year, now.month, now.day)
            tasks = TaskDB.objects.filter(
                Q(user_id=self.parent.id, is_my_day=True, status=False) |
                Q(finished_at__gte=start_date, status=True)
            ).order_by("-id")
        elif 'is_important' in data:
            tasks = TaskDB.objects.filter(
                user_id=self.parent.id, is_important=True).order_by("-id")
        elif 'tasks' in data:
            tasks = TaskDB.objects.filter(
                user_id=self.parent.id, task_list_id=0).order_by("-id")
        elif 'task_list_id' in data:
            tasks = TaskDB.objects.filter(
                user_id=self.parent.id, task_list_id=data["task_list_id"]).order_by("-id")
        elif 'keyword' in data:
            tasks = TaskDB.objects.filter(
                user_id=self.parent.id, name__icontains=data['keyword'], status=False).order_by("-id")
        else:
            return []
        return [Task(i) for i in tasks]

    def filter_suggest(self):
        """建议
        """

        tasks = TaskDB.objects.filter(user_id=self.parent.id, status=False, is_my_day=False).order_by("-id")
        return [Task(i) for i in tasks]
