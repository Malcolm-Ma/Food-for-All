from django.http import HttpResponse
import json
from Login.functions import check_login
from .functions import *

def get_user_info(request):
    response_data = user_info_dict
    user_info = check_login(request)
    if user_info:
        for i in response_data:
            response_data[i] = user_info.__getattribute__(i)
        response_data["region"] = RID2REGION[response_data["region"]]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def edit_user_info(request):
    response_data = {"status": edit_user_info_status["fail"]}
    user_info = check_login(request)
    if not user_info:
        response_data["status"] = edit_user_info_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    data = json.loads(request.body)
    edit_dict = {}
    for i in ("name", "region", "currency_type"):
        if i in data["edit"]:
            edit_dict[i] = data["edit"][i]
    if not update_user_info(filter_user_info({"uid": user_info.uid}), edit_dict):
        response_data["status"] = edit_user_info_status["fail"]
    else:
        response_data["status"] = edit_user_info_status["success"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")