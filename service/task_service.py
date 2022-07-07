from db.models import TaskList as  TaskListDB
class TaskService:

    @classmethod
    def fill(cls, dict_data, models):
        """
        填充数据
        """
        if "task_list" in dict_data:
            cls.fill_task_list(models)

    @classmethod
    def fill_task_list(cls, models):
        """
        填充task_list数据
        """
        task_list_ids = []
        for model in models:
            task_list_ids.append(model.task_list_id)

        task_lists = TaskListDB.objects.filter(id__in=task_list_ids).values("id", "name")
        task_list_dict = {}

        for model in task_lists:
            task_list_dict[model["id"]] = model["name"]

        for model in models:
            if model.task_list_id == 0:
                model.task_list = {"name": "任务"}
            else:
                model.task_list = {"name": task_list_dict[model.task_list_id]}
