from django.views import View
from django.http import JsonResponse
from business.task_list.task_list import TaskList
from business.task.task import Task as BTask


class Task(View):

    def get(self, request):
        task_id = request.GET["task_id"]
        task = request.god.task_repository.get_by_id(task_id)
        if not task:
            return JsonResponse({"errMsg": "未找到此任务"})
        data = {
            "id": task.id,
            "is_my_day": task.is_my_day,
            "is_important": task.is_important,
            "name": task.name,
            "deadline":  task.deadline,
            "notice": task.notice,
            "repeat": task.repeat,
            "remark": task.remark,
            "created_at": task.created_at,
            "status": task.status,
        }
        return JsonResponse({"data": data})

    def post(self, request):
        """可以添加task
        """
        json_data = request.json
        task = request.god.task_factory.create(json_data)

        if 'task_list_id' not in json_data:
            json_data["task_list_id"] = 0
        task_list = request.god.task_list_repository.get_by_id(
            json_data["task_list_id"])
        task_list.add_task(task)
        return JsonResponse({"data": ""}, status=201)

    def delete(self, request):
        """删除task"""
        json_data = request.json
        task = request.god.task_repository.get_by_id(json_data["task_id"])
        task_list = request.god.task_list_repository.get_by_id(task.task_list_id)
        task_list.delete_task(task)
        return JsonResponse({"data": ""}, status=201)

    def put(self, request):
        """更新task"""
        json_data = request.json
        task = request.god.task_repository.get_by_id(json_data["task_id"])
        if not task:
            return JsonResponse({"errMsg": "未找到此任务"}, status=404)
        data = {}

        if "deadline" in json_data:
            data["deadline"] = json_data["deadline"]["value"]
        if "notice" in json_data:
            data["notice"] = json_data["notice"]["value"]
        if "repeat" in json_data:
            data["repeat"] = json_data["repeat"]

        task.update(data)
        return JsonResponse({"data": ""}, status=201)

    def patch(self, request):
        """完成"""
        json_data = request.json
        op = json_data["op"]

        task = request.god.task_repository.get_by_id(json_data["task_id"])
        if not task:
            return JsonResponse({"errMsg": "未找到此任务"}, status=404)

        if op == "complete":
            task_list = request.god.task_list_repository.get_by_id(
                task.task_list_id)
            task_list.complete_task(task)
            return JsonResponse({"data": ""}, status=201)

        elif op == "uncomplete":
            task_list = request.god.task_list_repository.get_by_id(
                task.task_list_id)
            task_list.uncomplete_task(task)
            return JsonResponse({"data": ""}, status=201)
        elif op == "add_my_day":
            task.add_my_day()

        elif op == "delete_my_day":
            task.delete_my_day()

        elif op == "add_important":
            task.add_important()

        elif op == "delete_important":
            task.delete_important()

        elif op == 'update_remark':
            remark = json_data["remark"]
            task.update_remark(remark)

        return JsonResponse({"data": ""}, status=201)
