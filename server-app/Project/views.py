from django.http import HttpResponse, HttpResponseBadRequest
import json
from Login.functions import check_login
from .functions import *
import math

def get_projects(request):
    response_data = {"project_info": {},
                     "page_info": {"page": 1,
                                   "page_size": 1,
                                   "total_page": 1},
                     "currency_type": "GBP",
                     "order": {"current_order": "",
                               "orders": get_projects_orders("#")[0],
                               "separator": "#"},
                     "search": ""}
    if request.method == "GET":
        user = check_login(request)
        page_size = 20
        order = "-start_time"
        current_page = 1
        search = ""
        if user:
            currency_type = user.currency_type
        else:
            currency_type = CID2CURRENCY["GBP"]
    elif request.method == "POST":
        data = json.loads(request.body)
        order = data["order"]
        response_data["order"]["current_order"] = data["order"]
        search = data["search"]
        page_size = data["page_info"]["page_size"]
        current_page = data["page_info"]["page"]
        currency_type = data["currency_type"]
    else:
        return HttpResponseBadRequest()
    valid_projects = get_valid_projects()
    current_projects, filter_projects_num = get_current_projects_dict(valid_projects, current_page, page_size, order, search, currency_type)
    response_data["search"] = search
    response_data["currency_type"] = currency_type
    response_data["page_info"]["page"] = current_page
    response_data["page_info"]["page_size"] = page_size
    response_data["page_info"]["total_page"] = math.ceil(filter_projects_num / page_size)
    response_data["project_info"] = current_projects
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def get_project_info(request):
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {}
    data = json.loads(request.body)
    currency_type = data["currency_type"]
    pid = data["pid"]
    project = get_project({"pid": pid})
    if project:
        response_data = Project2dict(project, currency_type=currency_type)
    return HttpResponse(json.dumps(response_data), content_type="application/json")