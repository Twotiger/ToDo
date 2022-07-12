from django.views import View
from django.http import JsonResponse

class TaskList(View):
    
    def post(self, request):
        """可以添加taskGroup和taskList
        """
        json_data = request.json
        model = request.god.task_list_factory.create(json_data)
        data = request.god.task_list_repository.add_task_list(model)
        return JsonResponse({"data": ""}, status=201)

    def delete(self, request):
        json_data = request.json
        model = request.god.task_list_repository.get_by_id(json_data['id'])
        model.delete()
        return JsonResponse({"data": ''})