from django.shortcuts import render
from FoodForAll.settings import EXCHANGE_RATE
from Login.views import check_login
from DataBase import models
import json

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

def main(request):
    response_data = {"user_info": {"username":"",
                                   "name": "",
                                   "avatar": "",
                                   "type": 2,
                                   "region": ""},
                     "project_info": {},
                     "page_info": {"page": 1,
                                   "page_size": 1,
                                   "total_page": 1}
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
    if request.method == "GET":
        pass
