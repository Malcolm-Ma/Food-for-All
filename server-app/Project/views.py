from django.http import HttpResponse, HttpResponseBadRequest
import json
from Login.functions import check_login
from .functions import *
import math
from User.functions import update_user, user_type, add_project, remove_project

def get_projects_list(request):
    response_data = {"project_info": {},
                     "page_info": {"page": 1,
                                   "page_size": 1,
                                   "total_page": 1},
                     "currency_type": "GBP",
                     "order": {"current_order": "",
                               "orders": get_projects_orders("#")[0],
                               "separator": "#"},
                     "search": "",
                     "valid_only": 1}
    if request.method == "GET":
        user = check_login(request)
        page_size = 20
        order = "-start_time"
        current_page = 1
        search = ""
        uid = ""
        valid_only = 1
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
        uid = data["uid"]
        valid_only = data["valid_only"]
    else:
        return HttpResponseBadRequest()
    user = check_login(request)
    if valid_only:
        projects = get_valid_projects(uid=uid)
    else:
        projects = get_all_projects(uid=uid)
    current_projects, filter_projects_num = get_current_projects_dict(projects, current_page, page_size, order, search, currency_type)
    response_data["search"] = search
    response_data["valid_only"] = valid_only
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

def create_project(request):
    """
    @api {GET} /create_project/ create project
    @apiVersion 1.0.0
    @apiName create_project
    @apiGroup Project
    @apiDescription api for creating project by charity user

    @apiSuccess (200) {int} status Create status (0: success, 1: not_logged_in, 2: not_charity_user, 3: create_fail)
    @apiSuccess (200) {string} pid Pid of the project just created.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "pid": "fa00cb5f2e648afa9a39d99098c4fc84"
    }
    """
    response_data = {"status": "",
                     "pid": ""}
    user = check_login(request)
    if not user:
        response_data["status"] = create_project_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif user.type != user_type["charity"]:
        response_data["status"] = create_project_status["not_charity_user"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    project_dict = project_info_dict
    project_dict["uid"] = user.uid
    project_dict["region"] = user.region
    project_dict["charity"] = user.name
    project_dict["charity_avatar"] = user.avatar
    project_dict["region"] = user.region
    project_dict["pid"] = gen_pid(user.mail)
    if models.Project.objects.create(**project_dict):
        response_data["status"] = create_project_status["success"]
        response_data["pid"] = project_dict["pid"]
        add_project(user, project_dict["pid"])
    else:
        response_data["status"] = create_project_status["create_fail"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def delete_project(request):
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {"status": ""}
    user = check_login(request)
    if not user:
        response_data["status"] = delete_project_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif user.type != user_type["charity"]:
        response_data["status"] = delete_project_status["not_charity_user"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    data = json.loads(request.body)
    pid = data["pid"]
    project = get_project({"pid": pid})
    if not project:
        response_data["status"] = delete_project_status["project_not_exists"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    if project.uid != user.uid:
        response_data["status"] = delete_project_status["not_project_owner"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    project.delete()
    remove_project(user, pid)
    response_data["status"] = delete_project_status["success"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def edit_project_info(request):
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {"status": ""}
    user = check_login(request)
    if not user:
        response_data["status"] = edit_project_info_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    data = json.loads(request.body)
    pid = data["pid"]
    currency_type = data["currency_type"]
    project = get_project({"pid": pid})
    if not project:
        response_data["status"] = edit_project_info_status["project_not_exists"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    if project.uid != user.uid:
        response_data["status"] = edit_project_info_status["not_project_owner"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    edit_dict = {}
    for i in ("title", "intro", "background_image", "total_num", "start_time", "end_time", "details", "price"):
        if i in data["edit"]:
            edit_dict[i] = data["edit"][i]
    if "price" in edit_dict:
        cid = currency2cid(currency_type)
        if not cid:
            response_data["status"] = edit_project_info_status["wrong_currency_type"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        edit_dict["price"] = edit_dict["price"] / EXCHANGE_RATE[cid]
    if not update_project(project, edit_dict):
        response_data["status"] = edit_project_info_status["edit_fail"]
    else:
        response_data["status"] = edit_project_info_status["success"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")