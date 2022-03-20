import json
from django.http import HttpResponse, HttpResponseBadRequest
from .functions import *

def init_database(request):
    if request.method == "GET":
        user_num = 50
        project_num = 200
    elif request.method == "POST":
        data = json.loads(request.body)
        user_num = data["user_num"]
        project_num = data["project_num"]
    else:
        return HttpResponseBadRequest()
    init_database_with_fake_data(user_num, project_num)
    return HttpResponse(json.dumps({"user_num": user_num, "project_num": project_num}), content_type="application/json")