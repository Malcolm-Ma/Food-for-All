from django.shortcuts import render
from FoodForAll.settings import EXCHANGE_RATE
from django.db.models import F
from django.http import HttpResponse
from Login.views import check_login
from DataBase import models
import json
import math
import time

# Create your views here.
def projects_query2dict(project_query, currency_type="GBP"):
    projects = {}
    for i in range(project_query.count()):
        projects[str(i)] = {"pid": project_query[i].pid,
                            "uid": project_query[i].uid,
                            "title": project_query[i].title,
                            "charity": project_query[i].charity,
                            "intro": project_query[i].intro,
                            "region": project_query[i].region,
                            "charity_avatar": project_query[i].charity_avatar,
                            "background_image": project_query[i].background_image,
                            "price": project_query[i].price * EXCHANGE_RATE[currency_type],
                            "donation_num": {
                                "current": project_query[i].current_num,
                                "total": project_query[i].total_num,
                            },
                            "time": {
                                "start_time": project_query[i].start_time,
                                "end_time": project_query[i].end_time
                            }}
    return projects

def get_current_projects_dict(valid_projects, current_page, project_num, order, currency_type):
    current_projects = valid_projects.order_by(order)[(current_page - 1) * project_num: current_page * project_num]
    current_projects_dict = projects_query2dict(current_projects, currency_type)
    return current_projects_dict

def get_valid_projects():
    conditions = {"current_num__lt": F("total_num"), "end_time__lt": int(time.time())}
    valid_projects = models.Project.objects.filter(**conditions)
    return valid_projects

def main(request):
    response_data = {"user_info": {"username":"",
                                   "name": "",
                                   "avatar": "",
                                   "type": 2,
                                   "region": ""},
                     "project_info": {},
                     "page_info": {"page": 1,
                                   "page_size": 1,
                                   "total_page": 1},
                     "currency_type": "GBP"
                     }
    uid = check_login(request)
    if uid:
        user_info = models.User.objects.filter(uid=uid).first()
        response_data["user_info"]["username"] = user_info.mail
        response_data["user_info"]["name"] = user_info.name
        response_data["user_info"]["avatar"] = user_info.avatar
        response_data["user_info"]["type"] = user_info.type
        response_data["user_info"]["region"] = user_info.region
    data = json.loads(request.body)
    project_num = data["page_info"]["page_size"]
    response_data["page_info"]["page_size"] = project_num
    valid_projects = get_valid_projects()
    response_data["page_info"]["total_page"] = math.ceil(valid_projects.count() / project_num)
    if request.method == "GET":
        order = "-start_time"
        current_page = 1
        if uid:
            currency_type = user_info.currency_type
        else:
            currency_type = "GBP"
    elif request.method == "POST":
        order = data["order"]
        current_page = data["page_info"]["page"]
        currency_type = data["currency_type"]
    else:
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data["currency_type"] = currency_type
    response_data["page_info"]["page"] = current_page
    current_projects = get_current_projects_dict(valid_projects, current_page, project_num, order, currency_type)
    response_data["project_info"] = current_projects
    return HttpResponse(json.dumps(response_data), content_type="application/json")