from DataBase import models
import time
from django.db.models import F, Q
from Common.common import *
from hashlib import md5

create_project_status = {"success": 0,
                         "not_logged_in": 1,
                         "not_charity_user": 2,
                         "create_fail": 3}

delete_project_status = {"success": 0,
                         "not_logged_in": 1,
                         "not_charity_user": 2,
                         "project_not_exists": 3,
                         "not_project_owner": 4,
                         "not_deletable": 5}

edit_project_info_status = {"success": 0,
                            "not_logged_in": 1,
                            "wrong_currency_type": 2,
                            "project_not_exists": 3,
                            "not_project_owner": 4,
                            "edit_fail": 5,
                            "not_editable": 6}

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

def project2dict(project, fields=(), currency_type=""):
    project_dict = {}
    for i in copy.deepcopy(project_info_dict):
        if i in fields or len(fields) == 0:
            project_dict[i] = project.__getattribute__(i)
    if "price" in fields or len(fields) == 0:
        cid = currency2cid(currency_type)
        if cid:
            project_dict["price"] = project_dict["price"] * EXCHANGE_RATE[cid]
        else:
            return {}
    if "region" in fields or len(fields) == 0:
        project_dict["region"] = rid2region(project_dict["region"])
    if "donate_history" in fields or len(fields) == 0:
        project_dict["donate_history"] = eval(project_dict["donate_history"])
    if "status" in fields or len(fields) == 0:
        if project_dict["status"] == PROJECT_STATUS["ongoing"] and (project.current_num >= project.total_num or project.end_time <= int(time.time())):
            project_dict["status"] = PROJECT_STATUS["finish"]
            project.status = PROJECT_STATUS["finish"]
            project.save(fields=["status"])
    return project_dict

def projects_query2dict(projects_query, currency_type=CID2CURRENCY["GBP"]):
    projects = {}
    cid = currency2cid(currency_type)
    if cid:
        for i in range(len(projects_query)):
            projects[str(i)] = project2dict(projects_query[i], fields=["pid", "title", "intro", "region",
                                            "charity", "charity_avatar", "background_image", "price",
                                            "current_num", "total_num", "start_time", "end_time", "status"],
                                            currency_type=currency_type)
    return projects

def get_all_projects(uid=""):
    if uid:
        projects = models.Project.objects.filter(uid=uid)
    else:
        projects = models.Project.objects.all()
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
    filtered_projects = models.Project.objects.filter(**filter_conditions).exclude(**exclude_conditions)
    return filtered_projects

def get_prepare_projects(uid):
    return models.Project.objects.filter(**{"uid": uid, "status": PROJECT_STATUS["prepare"]})

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

# def update_projects_query_status(projects):
#     projects_outdated = projects.filter(**{"status": PROJECT_STATUS["ongoing"]}).filter(Q(current_num__gte = F("total_num")) | Q(end_time__lte = int(time.time())))
#     projects_outdated.update(**{"status": PROJECT_STATUS["finish"]})
#     return projects

def gen_pid(seq=""):
    id = md5((str(time.time()) + seq).encode("utf-8")).hexdigest()
    if models.Project.objects.filter(pid=id):
        id = gen_pid(seq=seq)
    return id

def get_project(filter_dict):
    if len(filter_dict) != 1 or "pid" not in filter_dict:
        return ""
    try:
        r = models.Project.objects.get(**filter_dict)
        return r
    except:
        return ""

def update_project(project, update_dict):
    update_keys_list = ["title", "intro", "background_image", "total_num", "start_time", "end_time", "details", "price"]
    for key in update_dict.keys():
        if key not in update_keys_list:
            return False
    try:
        for i in update_dict:
            project.__setattr__(i, update_dict[i])
        project.save(update_fields=list(update_dict.keys()))
        return True
    except:
        return False