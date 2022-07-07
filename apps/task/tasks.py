
from django.views import View
from django.http import JsonResponse
from business.task_list.task_list import TaskList
from service.task_service import TaskService


class TasksSuggest:

    @classmethod
    def get_tasks(cls, request):
        models = request.god.task_repository.filter_suggest()
        TaskService.fill({"task_list": True}, models)
        data = []
        for model in models:
            data.append({
                "id": model.id,
                "name": model.name,
                "deadline": model.deadline,
                "repeat": model.repeat,
                "notice": model.notice,
                'is_my_day': model.is_my_day,
                'is_important': model.is_important,
                "task_list": model.task_list,
            })
        return data


class TasksSearch:

    @classmethod
    def get_tasks(cls, request):
        models = request.god.task_repository.filter(request.GET)
        TaskService.fill({"task_list": True}, models)

        data = []  # [{'name': ss, data: []},{}]
        mem = {}
        for model in models:
            key = model.task_list.get('name', '')
            mem.setdefault(key, [])
            mem[key].append({
                "id": model.id,
                "name": model.name,
                "deadline": model.deadline,
                "repeat": model.repeat,
                "notice": model.notice,
                'is_my_day': model.is_my_day,
                'is_important': model.is_important,
                "task_list": model.task_list,
            })

        for key, value in mem.items():
            data.append({
                "name": key, 'data': value
            })
        return data


class Tasks(View):

    def get(self, request):
        """
        """
        suggest = request.GET.get('suggest') # 建议
        if suggest:

            data = TasksSuggest.get_tasks(request)
            return JsonResponse({"data": data}, status=200)

        keyword = request.GET.get('keyword') # 搜索关键字
        if keyword:
            data = TasksSearch.get_tasks(request)
            return JsonResponse({"data": data}, status=200)

        task_list = request.god.task_list_repository.get_by_id(
            request.GET.get("task_list_id", 0))
        if task_list is None:
            return JsonResponse({"errMsg": "非法的task_list_id"}, status=404)
        models = request.god.task_repository.filter(request.GET)
        TaskService.fill({"task_list": True}, models)
        data = []
        completed = []
        for model in models:
            if model.status:
                completed.append({
                    "id": model.id,
                    "name": model.name,
                    "deadline": model.deadline,
                    "repeat": model.repeat,
                    "notice": model.notice,
                    'is_my_day': model.is_my_day,
                    'is_important': model.is_important,
                    "task_list": model.task_list,
                })
            else:
                data.append({
                    "id": model.id,
                    "name": model.name,
                    "deadline": model.deadline,
                    "repeat": model.repeat,
                    "notice": model.notice,
                    'is_my_day': model.is_my_day,
                    'is_important': model.is_important,
                    "task_list": model.task_list,
                })

        return JsonResponse({"uncompleted": data, "completed": completed, "name": task_list.name}, status=200)
