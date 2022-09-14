import json
from pytz import utc
from datetime import timedelta, datetime, timezone

from utils.business_model import Model
from utils.decorator import cached_property
from db.models import Task as TaskDB, TaskList, DEFAULT_DATE
from event.task_event import TaskEvent


class Task(Model):

    __slots__ = ("id", "name", "is_my_day", "is_important",
                 "deadline", "notice", "repeat", "status", "remark", "task_list_id", "user_id", "created_at")

    def __init__(self, db_model=None):
        super().__init__(db_model)
        if not db_model:
            return
        if db_model.deadline.year == 1:
            self.deadline = ''
        if db_model.notice.year == 1:
            self.notice = ''
        try:
            json_data = json.loads(db_model.repeat)
            if json_data['intervalType'] == '':
                self.repeat = {}
            else:
                self.repeat = json_data
        except:
            self.repeat = {}

    @cached_property
    def task_list(self):
        if self.task_list_id == 0:
            return {}
        model = TaskList.objects.filter(id=self.task_list_id).first()
        return {"name": model.name}

    def complete(self):
        """完成任务
        如果是循环任务,需要创建另一个
        """
        TaskDB.objects.filter(
            id=self.id, user_id=self.user_id).update(status=True, finished_at=datetime.now())

    def uncomplete(self):
        """未完成"""
        TaskDB.objects.filter(
            id=self.id, user_id=self.user_id).update(status=False, finished_at=DEFAULT_DATE)

    def add_my_day(self):
        TaskDB.objects.filter(
            id=self.id, user_id=self.user_id).update(is_my_day=True)

    def delete_my_day(self):
        TaskDB.objects.filter(
            id=self.id, user_id=self.user_id).update(is_my_day=False)

    def add_important(self):
        TaskDB.objects.filter(
            id=self.id, user_id=self.user_id).update(is_important=True)

    def delete_important(self):
        TaskDB.objects.filter(id=self.id, user_id=self.user_id).update(
            is_important=False)

    def update_remark(self, remark):
        TaskDB.objects.filter(
            id=self.id, user_id=self.user_id).update(remark=remark)


    def update(self, data):
        # TODO 验证重复
        """
        如果原来没有,现在有就添加
        如果原来有,现在也有就修改
        如果原来有,现在没有就删除
        """
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if 'notice' in data:
            if not self.notice:
                dt = datetime.strptime(data['notice'], FORMAT)
                dt_new = dt.replace(tzinfo=utc)
                self.notice = dt_new

                TaskEvent.add_notice_job(self)
            elif self.notice and data['notice'] != '':
                dt = datetime.strptime(data['notice'], FORMAT)
                dt_new = dt.replace(tzinfo=utc)
                self.notice = dt_new
                TaskEvent.modify_notice_job(self)
                
            elif self.notice and data["notice"] == '':
                TaskEvent.del_notice_job(self)

        if self.notice:
            pass

        if 'deadline' in data and data['deadline'] == '':
            data['deadline'] = datetime(1, 1, 1, tzinfo=timezone.utc)
        if 'notice' in data and data['notice'] == '':
            data['notice'] = datetime(1, 1, 1, tzinfo=timezone.utc)
        if 'repeat' in data:
            data['repeat'] = json.dumps(data['repeat'])

        TaskDB.objects.filter(id=self.id).update(**data)
