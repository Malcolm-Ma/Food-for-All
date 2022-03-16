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
                               "separator": "#"}}
    if request.method == "GET":
        user_info = check_login(request)
        page_size = 20
        order = "-start_time"
        current_page = 1
        if user_info:
            currency_type = user_info.currency_type
        else:
            currency_type = CID2CURRENCY["GBP"]
    elif request.method == "POST":
        data = json.loads(request.body)
        order = data["order"]
        response_data["order"]["current_order"] = data["order"]
        page_size = data["page_info"]["page_size"]
        current_page = data["page_info"]["page"]
        currency_type = data["currency_type"]
    else:
        return HttpResponseBadRequest()
    valid_projects = get_valid_projects()
    current_projects = get_current_projects_dict(valid_projects, current_page, page_size, order, currency_type)
    response_data["currency_type"] = currency_type
    response_data["page_info"]["page"] = current_page
    response_data["page_info"]["page_size"] = page_size
    response_data["page_info"]["total_page"] = math.ceil(valid_projects.count() / page_size)
    response_data["project_info"] = current_projects
    return HttpResponse(json.dumps(response_data), content_type="application/json")