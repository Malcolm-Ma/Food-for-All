from DataBase import models
import time
from django.db.models import F
from FoodForAll.settings import EXCHANGE_RATE, RID2REGION, CID2CURRENCY, CURRENCY2CID

def projects_query2dict(projects_query, currency_type=CID2CURRENCY["GBP"]):
    projects = {}
    if currency_type in CURRENCY2CID:
        for i in range(projects_query.count()):
            projects[str(i)] = {"pid": projects_query[i].pid,
                                "uid": projects_query[i].uid,
                                "title": projects_query[i].title,
                                "charity": projects_query[i].charity,
                                "intro": projects_query[i].intro,
                                "region": RID2REGION[projects_query[i].region],
                                "charity_avatar": projects_query[i].charity_avatar,
                                "background_image": projects_query[i].background_image,
                                "price": projects_query[i].price * EXCHANGE_RATE[CURRENCY2CID[currency_type]],
                                "donation_num": {
                                    "current": projects_query[i].current_num,
                                    "total": projects_query[i].total_num,
                                },
                                "time": {
                                    "start_time": projects_query[i].start_time,
                                    "end_time": projects_query[i].end_time
                                }}
    return projects

def get_valid_projects():
    conditions = {"current_num__lt": F("total_num"), "end_time__gt": int(time.time()), "start_time__lt": int(time.time())}
    valid_projects = models.Project.objects.filter(**conditions)
    return valid_projects

def get_ordered_projects(projects, order):
    return projects.order_by(order)

def get_current_projects_dict(valid_projects, current_page, project_num, order, currency_type):
    current_projects = get_ordered_projects(valid_projects, order)
    current_projects = current_projects[(current_page - 1) * project_num: min(current_page * project_num, current_projects.count())]
    current_projects_dict = projects_query2dict(current_projects, currency_type)
    return current_projects_dict