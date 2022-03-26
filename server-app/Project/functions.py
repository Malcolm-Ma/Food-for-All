from DataBase.models import *
import time
from django.db.models import F, Q
from Common.common import *
from hashlib import md5

project_info_dict = {"pid": "",
                     "uid": "",
                     "title": "",
                     "intro": "",
                     "region": "",
                     "charity": "",
                     "charity_avatar": "",
                     "background_image": "",
                     "status": 0,
                     "details": "",
                     "price": 0,
                     "donate_history": {},
                     "current_num": 0,
                     "total_num": 0,
                     "start_time": 0,
                     "end_time": 0}

projects_orders = ["title", "-title", "charity", "-charity", "price", "-price",
                   "start_time", "-start_time", "end_time", "-end_time", "progress", "-progress"]

def projects_query2dict(projects_query, currency_type=CID2CURRENCY["GBP"]):
    projects = {}
    cid = currency2cid(currency_type)
    if cid:
        for i in range(len(projects_query)):
            projects[str(i)] = projects_query[i].to_dict(fields=["pid", "title", "intro", "region",
                                            "charity", "charity_avatar", "background_image", "price",
                                            "current_num", "total_num", "start_time", "end_time", "status"],
                                            currency_type=currency_type)
    return projects

def get_all_projects(uid=""):
    if uid:
        projects = DProject.objects.filter(uid=uid)
    else:
        projects = DProject.objects.all()
    return projects

def get_filtered_projects(uid="", valid_only=1):
    exclude_conditions = {}
    filter_conditions = {}
    if valid_only:
        filter_conditions.update({"status": PROJECT_STATUS["ongoing"], "current_num__lt": F("total_num"), "end_time__gt": int(time.time())})
    else:
        exclude_conditions.update({"status": PROJECT_STATUS["prepare"]})
    if uid:
        filter_conditions.update({"uid": uid})
    filtered_projects = DProject.objects.filter(**filter_conditions).exclude(**exclude_conditions)
    return filtered_projects

def get_prepare_projects(uid):
    return DProject.objects.filter(**{"uid": uid, "status": PROJECT_STATUS["prepare"]})

def get_ordered_projects(projects, order):
    if order not in projects_orders:
        return None
    elif order == "progress":
        order = F('current_num') / F('total_num')
    elif order == "-progress":
        order = -F('current_num') / F('total_num')
    return projects.order_by(order)

def get_searched_projects(projects, search):
    if search == "":
        return projects
    q=Q()
    for w in search.split():
        q = q | Q(title__icontains = w) | Q(intro__icontains = w) | Q(charity__icontains = w)# | Q(details__icontains = w)
    searched_projects = projects.filter(q)
    return searched_projects

def get_current_projects_dict(filtered_projects, current_page, project_num, order, search, currency_type):
    ordered_projects = get_ordered_projects(filtered_projects, order)
    if search != "":
        searched_projects = get_searched_projects(ordered_projects, search)
    else:
        searched_projects = ordered_projects
    if not searched_projects:
        return {}, 0
    filter_projects_num = len(searched_projects)
    current_projects = searched_projects[(current_page - 1) * project_num: min(current_page * project_num, filter_projects_num)]
    current_projects_dict = projects_query2dict(current_projects, currency_type)
    return current_projects_dict, filter_projects_num