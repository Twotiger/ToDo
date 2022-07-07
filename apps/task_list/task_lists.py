from django.views import View
from django.http import JsonResponse
# from business.task_list.task_list import TaskList
from service.task_list_service import TaskListService


class TaskLists(View):

    def get(self, request):

        models = request.god.task_list_repository.filter()

        data = []
        mem = {}
        for model in models:

            if model.task_type == "group" or model.parent_id == 0:
                # 表示最外层
                task_list = {"name": model.name, "id": model.id,
                             "children": [], "task_type": model.task_type}
                if hasattr(model, "count"):
                    task_list["count"] = model.count
                data.append(task_list)
                mem[model.id] = task_list

            else:
                mem[model.parent_id]["children"].append({"name": model.name, "id": model.id,
                                                         "task_type": model.task_type, "count": model.count})

        return JsonResponse({"data": data, "task_count": request.god.get_task_count()})

    def patch(self, request):
        """移动位置
        将两个个task_list交换位置
        将task_list移动到task_group中
        将task_list从task_group中移出
        """

        json_data = request.json
        from_id = json_data["from_id"]
        to_id = json_data["to_id"]
        position = json_data["position"]

        from_task_list = request.god.task_list_repository.get_by_id(from_id)
        to_task_list = request.god.task_list_repository.get_by_id(to_id)

        is_success, msg = TaskListService.change_position(
            from_task_list, to_task_list, position)
        if not is_success:
            return JsonResponse({"errMsg": msg}, status=400)
        return JsonResponse({"data": ""}, status=201)
