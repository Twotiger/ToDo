"""
在Request实例中添加json属性
"""
import json


class JSONMethod:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method in (
            "POST",
            "DELETE",
            "PUT",
            "PATCH",
         ) and 'application/json' in request.content_type:
            try:
                json_data = json.loads(request.body.decode("utf-8"))
                request.json = json_data
            except Exception as e:
                print(e) # TODO 删除

        return self.get_response(request)
