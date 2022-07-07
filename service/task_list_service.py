from django.db.models import F
from business.task.task import Task
from db.models import TaskList as TaskListDB
from business.task_list.task_list import TaskList


class TaskListService():

    @classmethod
    def task_list_update_count(cls, task_list_id: int, count: int):
        """
        更新task_list的count
        """
        task_list = TaskListDB.objects.get(id=task_list_id)
        task_list.count = count
        task_list.save()

    @classmethod
    def check_change_position(cls, from_task_list: TaskList, to_task_list: TaskList, position: str):
        """
        检查是否可以更改位置
        """
        if from_task_list.id == to_task_list.id:
            return False, "不能移动到自己"

        # 不可以移动到列表里面
        if to_task_list.task_type == 'list' and position == 'in':
            return False, "不可以移动到列表里面"

        if from_task_list.task_type == 'group' and position == 'in':
            return False, "组不可以移动到里面"

        if from_task_list.task_type == 'group' and to_task_list.parent_id != 0:
            return False, "组不可以移动到里面"

        if position == 'in':
            if TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=to_task_list.id).exists():
                return False, "操作错误"

        return True,  ''

    @classmethod
    def change_position(cls, from_task_list: TaskList, to_task_list: TaskList, position: str):
        """
        修改task_list的位置
        """
        res, msg = cls.check_change_position(
            from_task_list, to_task_list, position)
        if not res:
            return res, msg

        if position == "in":
            cls.move_in(from_task_list, to_task_list)
        else:

            if position == 'up':
                if to_task_list.index == 1:
                    new_to_task_list = TaskList()
                    new_to_task_list.index = 0
                    new_to_task_list.parent_id = to_task_list.parent_id
                else:
                    new_to_task_list = TaskList()
                    new_to_task_list.index = to_task_list.index - 1
                    new_to_task_list.parent_id = to_task_list.parent_id
            else:
                new_to_task_list = to_task_list

            if from_task_list.parent_id == 0 and to_task_list.parent_id == 0:
                cls.first_to_first(from_task_list=from_task_list,
                                   to_task_list=new_to_task_list)

            elif from_task_list.parent_id == 0 and to_task_list.parent_id != 0:
                cls.first_to_second(from_task_list, new_to_task_list)

            elif from_task_list.parent_id != 0 and to_task_list.parent_id == 0:
                cls.second_to_first(from_task_list, new_to_task_list)

            elif from_task_list.parent_id != 0 and to_task_list.parent_id != 0:
                cls.second_to_second(from_task_list, to_task_list)
            else:
                raise ValueError("不可能的情况")
        return True, ''

    @classmethod
    def first_to_second(cls, from_task_list, to_task_list):
        """
        第一层移动到第二层
        """

        TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=to_task_list.parent_id,
                                  index__gt=to_task_list.index).update(index=F('index') + 1)
        TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=0,
                                  index__gt=from_task_list.index).update(index=F("index") - 1)
        TaskListDB.objects.filter(id=from_task_list.id).update(
            parent_id=to_task_list.parent_id, index=to_task_list.index+1)

    @classmethod
    def second_to_first(cls, from_task_list, to_task_list):
        """
        第二层移动到第一层
        """
        # 移动第二层
        TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=from_task_list.parent_id,
                                  index__gt=from_task_list.index).update(index=F('index') - 1)
        # 移动第一层
        TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=0,
                                  index__gt=to_task_list.index).update(index=F("index") + 1)
        TaskListDB.objects.filter(id=from_task_list.id).update(
            parent_id=0, index=to_task_list.index+1)

    @classmethod
    def second_to_second(cls, from_task_list, to_task_list):
        """
        第二层移动到第二层
        """
        TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=to_task_list.parent_id,
                                  index__gt=to_task_list.index).update(index=F('index') + 1)

        TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=to_task_list.parent_id,
                                  index__gt=from_task_list.index).update(index=F('index') - 1)

        TaskListDB.objects.filter(id=from_task_list.id).update(
            parent_id=to_task_list.parent_id, index=to_task_list.index+1)

    @classmethod
    def first_to_first(cls, from_task_list: TaskList, to_task_list: TaskList):
        """
        第一层移动到第一层
        """
        if from_task_list.index > to_task_list.index:
            # 大的向小的移动,要加
            TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=0,
                                      index__gt=to_task_list.index, index__lt=from_task_list.index).update(index=F('index') + 1)
            TaskListDB.objects.filter(id=from_task_list.id).update(
                index=to_task_list.index+1)
        else:
            TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=0,
                                      index__gt=from_task_list.index, index__lte=to_task_list.index).update(index=F('index') - 1)
            TaskListDB.objects.filter(id=from_task_list.id).update(
                index=to_task_list.index)

    @classmethod
    def move_in(cls, from_task_list: TaskList, to_task_list: TaskList):
        """
        移动task_list到task_group中
        """

        # 移动from
        TaskListDB.objects.filter(user_id=from_task_list.user_id, parent_id=from_task_list.parent_id,
                                  index__gt=from_task_list.index).update(index=F("index") - 1)
        # 移动to
        TaskListDB.objects.filter(id=from_task_list.id).update(
            parent_id=to_task_list.id, index=1)
