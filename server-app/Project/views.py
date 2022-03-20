from django.http import HttpResponse, HttpResponseBadRequest
import json
from Login.functions import check_login
from .functions import *
import math
from User.functions import update_user, add_project, remove_project

@api_logger(logger=logger_standard)
def get_projects_list(request):
    """
    @api {GET, POST} /get_projects_list/ get projects list
    @apiVersion 1.0.0
    @apiName get_projects_list
    @apiGroup Project
    @apiDescription api to get projects list by conditions

    @apiParam {String} order The way the list of projects is ordered. It should be included in the "order_list" provided by this interface.
    @apiParam {String} currency_type Currency type. It should be included in the list provided by "currency_list/" interface.
    @apiParam {Dict} page_info Information of pages. Its sub-parameters are shown below.
    @apiParam {Int} page_size (Sub-parameter of page_info) Number of projects displayed per page.
    @apiParam {Int} page (Sub-parameter of page_info) Current page number.
    @apiParam {String} search The string to be retrieved. It should be set to "" when the search action has not occurred.
    @apiParam {Int} valid_only Whether only valid projects are displayed. (0: False, 1: True)
    @apiParam {String} uid If searching only for projects owned by a particular user, set this parameter to the uid of the corresponding user, otherwise set it to "".

    @apiSuccess (Success 200 return) {Dict} project_info Projects list. The keys of this dictionary are the order of the projects counting from 0 and the values are the information of the projects corresponding to their order. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} pid (Sub-parameter of project_info) Pid of the project.
    @apiSuccess (Success 200 return) {String} title (Sub-parameter of project_info) Title of project.
    @apiSuccess (Success 200 return) {String} intro (Sub-parameter of project_info) Introduction of project.
    @apiSuccess (Success 200 return) {String} region (Sub-parameter of project_info) Country or region of the project's owner. It should be included in the list provided by "region_list/" interface.
    @apiSuccess (Success 200 return) {String} charity (Sub-parameter of project_info) Name of the project's owner.
    @apiSuccess (Success 200 return) {String} charity_avatar (Sub-parameter of project_info) Static avatar url of the project's owner.
    @apiSuccess (Success 200 return) {String} background_image (Sub-parameter of project_info) Static background image url of the project.
    @apiSuccess (Success 200 return) {Float} price (Sub-parameter of project_info) The single donation price of the project.
    @apiSuccess (Success 200 return) {Int} current_num (Sub-parameter of project_info) Number of donations accepted.
    @apiSuccess (Success 200 return) {Int} total_num (Sub-parameter of project_info) The total number of donations expected to be received and the project ends when this number is reached.
    @apiSuccess (Success 200 return) {Int} start_time (Sub-parameter of project_info) The time at which the project starts and before which the project will not be shown.
    @apiSuccess (Success 200 return) {Int} end_time (Sub-parameter of project_info) The time at which the project will end. When this time is reached, the project will be closed even if it has not reached the desired number of donations.
    @apiSuccess (Success 200 return) {Dict} page_info Information of pages. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {Int} page_size (Sub-parameter of page_info) Number of projects displayed per page.
    @apiSuccess (Success 200 return) {Int} total_page (Sub-parameter of page_info) Total number of pages.
    @apiSuccess (Success 200 return) {Int} page (Sub-parameter of page_info) Current page number.
    @apiSuccess (Success 200 return) {String} currency_type Currency type. It should be included in the list provided by "currency_list/" interface.
    @apiSuccess (Success 200 return) {Dict} order Information of the ways the list of projects is ordered. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} current_order (Sub-parameter of order) Current way the list of projects is ordered. It should be included in the "order_list" below.
    @apiSuccess (Success 200 return) {List(String)} order_list (Sub-parameter of order) List of allowed sorting methods. ("title", "-title", "charity", "-charity", "price", "-price", "start_time", "-start_time", "end_time", "-end_time", "progress", "-progress")
    @apiSuccess (Success 200 return) {String} search The string has been retrieved. It would be set to "" when the search action has not occurred.
    @apiSuccess (Success 200 return) {Int} valid_only Whether only valid projects are displayed. (0: False, 1: True)

    @apiParamExample {Json} Sample Request
    {
        "order": "-progress",
        "currency_type": "CNY (Chinese Yuan Renminbi)",
        "page_info": {
                "page_size": 5,
                "page": 1
                },
        "search": "qwer",
        "valid_only": 1,
        "uid": ""
    }
    @apiSuccessExample {Json} Response-Success
    {
        "project_info": {
            "0": {
                "pid": "d48b0eac410514a8b032fd41bd20c1dc",
                "title": "3",
                "intro": "qwer3",
                "region": "CN",
                "charity": "3",
                "charity_avatar": "",
                "background_image": "",
                "price": 24.7987350414,
                "current_num": 3,
                "total_num": 100,
                "start_time": 1647558799,
                "end_time": 1679094899
            },
            "1": {
                "pid": "9dfd14feba9c9822377262fdf76e2c1c",
                "title": "13",
                "intro": "qwer13",
                "region": "CN",
                "charity": "13",
                "charity_avatar": "",
                "background_image": "",
                "price": 107.4611851794,
                "current_num": 13,
                "total_num": 100,
                "start_time": 1647558809,
                "end_time": 1679094909
            },
            "2": {
                "pid": "3494c5b8f941afb1a228260861d9f7d9",
                "title": "23",
                "intro": "23",
                "region": "CN",
                "charity": "23qwer",
                "charity_avatar": "",
                "background_image": "",
                "price": 190.12363531740002,
                "current_num": 23,
                "total_num": 100,
                "start_time": 1647558819,
                "end_time": 1679094919
            },
            "3": {
                "pid": "31f0b2737b1249ce207ff64eba63cb47",
                "title": "30",
                "intro": "30qwer",
                "region": "CN",
                "charity": "30",
                "charity_avatar": "",
                "background_image": "",
                "price": 247.98735041400002,
                "current_num": 30,
                "total_num": 100,
                "start_time": 1647558826,
                "end_time": 1679094926
            },
            "4": {
                "pid": "8dcad1d3db4dc77241eecc82a9310a73",
                "title": "31qwer",
                "intro": "31",
                "region": "CN",
                "charity": "31",
                "charity_avatar": "",
                "background_image": "",
                "price": 256.2535954278,
                "current_num": 31,
                "total_num": 100,
                "start_time": 1647558827,
                "end_time": 1679094927
            }
        },
        "page_info": {
            "page": 1,
            "page_size": 5,
            "total_page": 3
        },
        "currency_type": "CNY (Chinese Yuan Renminbi)",
        "order": {
            "current_order": "progress",
            "order_list": [
                "title",
                "-title",
                "charity",
                "-charity",
                "price",
                "-price",
                "start_time",
                "-start_time",
                "end_time",
                "-end_time",
                "progress",
                "-progress"
            ]
        },
        "search": "qwer",
        "valid_only": 1
    }
    """
    response_data = {"project_info": {},
                     "page_info": {"page": 1,
                                   "page_size": 1,
                                   "total_page": 1},
                     "currency_type": "GBP",
                     "order": {"current_order": "",
                               "order_list": projects_orders},
                     "search": "",
                     "valid_only": 1}
    if request.method == "GET":
        page_size = 20
        order = "-start_time"
        current_page = 1
        search = ""
        uid = ""
        valid_only = 1
        currency_type = ""
    elif request.method == "POST":
        data = json.loads(request.body)
        order = data["order"] if data["order"] else "-start_time"
        response_data["order"]["current_order"] = order
        search = data["search"]
        page_size = data["page_info"]["page_size"] if data["page_info"]["page_size"] else 20
        current_page = data["page_info"]["page"] if data["page_info"]["page"] else 1
        currency_type = data["currency_type"]
        uid = data["uid"]
        valid_only = data["valid_only"]
    else:
        return HttpResponseBadRequest()
    user = check_login(request)
    if user and not currency2cid(currency_type):
        currency_type = user.currency_type
    else:
        currency_type = CID2CURRENCY["GBP"]
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

@api_logger(logger=logger_standard)
def get_project_info(request):
    """
    @api {POST} /get_project_info/ get project information
    @apiVersion 1.0.0
    @apiName get_project_info
    @apiGroup Project
    @apiDescription api to get project details

    @apiParam {String} pid Pid of the project.
    @apiParam {String} currency_type Currency type. It should be included in the list provided by "currency_list/" interface.

    @apiSuccess (Success 200 return) {String} pid Pid of the project.
    @apiSuccess (Success 200 return) {String} uid Uid of the project's owner.
    @apiSuccess (Success 200 return) {String} title Title of project.
    @apiSuccess (Success 200 return) {String} intro Introduction of project.
    @apiSuccess (Success 200 return) {String} region Country or region of the project's owner. It should be included in the list provided by "region_list/" interface.
    @apiSuccess (Success 200 return) {String} charity Name of the project's owner.
    @apiSuccess (Success 200 return) {String} charity_avatar Static avatar url of the project's owner.
    @apiSuccess (Success 200 return) {String} background_image Static background image url of the project.
    @apiSuccess (Success 200 return) {String} details Details of the project, containing rich text information.
    @apiSuccess (Success 200 return) {Float} price The single donation price of the project.
    @apiSuccess (Success 200 return) {Dict} donate_history Donate history. The data format is {string: {string: int}}, i.e. {uid: {timestamp: num}}. This means that the user "uid" donated "num" times to the project at time "timestamp".
    @apiSuccess (Success 200 return) {Int} current_num Number of donations accepted.
    @apiSuccess (Success 200 return) {Int} total_num The total number of donations expected to be received and the project ends when this number is reached.
    @apiSuccess (Success 200 return) {Int} start_time The time at which the project starts and before which the project will not be shown.
    @apiSuccess (Success 200 return) {Int} end_time The time at which the project will end. When this time is reached, the project will be closed even if it has not reached the desired number of donations.

    @apiParamExample {Json} Sample Request
    {
        "pid": "360a27773752a7a025b3cd3d931f26e2",
        "currency_type": "USD"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "pid": "360a27773752a7a025b3cd3d931f26e2",
        "uid": "506d201c0d8d23fcee2a4bada084acae",
        "title": "49",
        "intro": "49",
        "region": "GB",
        "charity": "qwer",
        "charity_avatar": "",
        "background_image": "",
        "details": "49",
        "price": 63.8893964219,
        "donate_history": {},
        "current_num": 49,
        "total_num": 100,
        "start_time": 1647549001,
        "end_time": 1679085101
    }
    """
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {}
    data = json.loads(request.body)
    currency_type = data["currency_type"]
    pid = data["pid"]
    project = get_project({"pid": pid})
    if project:
        response_data = project2dict(project, currency_type=currency_type)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger(logger=logger_standard)
def create_project(request):
    """
    @api {GET} /create_project/ create project
    @apiVersion 1.0.0
    @apiName create_project
    @apiGroup Project
    @apiDescription api for creating project by charity user

    @apiSuccess (Success 200 return) {Int} status Create status (0: success, 1: not_logged_in, 2: not_charity_user, 3: create_fail)
    @apiSuccess (Success 200 return) {String} pid Pid of the project just created.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "pid": "fa00cb5f2e648afa9a39d99098c4fc84"
    }
    """
    if request.method != "GET":
        return HttpResponseBadRequest()
    response_data = {"status": "",
                     "pid": ""}
    user = check_login(request)
    if not user:
        response_data["status"] = create_project_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif user.type != USER_TYPE["charity"]:
        response_data["status"] = create_project_status["not_charity_user"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    project_dict = project_info_dict
    project_dict["uid"] = user.uid
    project_dict["region"] = user.region
    project_dict["charity"] = user.name
    project_dict["charity_avatar"] = user.avatar
    project_dict["region"] = user.region
    project_dict["donate_history"] = "{}"
    project_dict["pid"] = gen_pid(user.mail)
    if models.Project.objects.create(**project_dict):
        response_data["status"] = create_project_status["success"]
        response_data["pid"] = project_dict["pid"]
        add_project(user, project_dict["pid"])
    else:
        response_data["status"] = create_project_status["create_fail"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger(logger=logger_standard)
def delete_project(request):
    """
    @api {POST} /delete_project/ delete project
    @apiVersion 1.0.0
    @apiName delete_project
    @apiGroup Project
    @apiDescription api to delete project by its owner

    @apiParam {String} pid Pid of the project.

    @apiSuccess (Success 200 return) {Int} status Delete status (0: success, 1: not_logged_in, 2: not_charity_user, 3: project_not_exists, 4: not_project_owner)

    @apiParamExample {Json} Sample Request
    {
        "pid": "b42fcd36aac47bfafdd6b7a543c55c30"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {"status": ""}
    user = check_login(request)
    if not user:
        response_data["status"] = delete_project_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif user.type != USER_TYPE["charity"]:
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

@api_logger(logger=logger_standard)
def edit_project_info(request):
    """
    @api {POST} /edit_project_info/ edit project information
    @apiVersion 1.0.0
    @apiName edit_project_info
    @apiGroup Project
    @apiDescription api for editing project information by its owner

    @apiParam {String} pid Pid of the project.
    @apiParam {String} currency_type Currency type. It should be included in the list provided by "currency_list/" interface.
    @apiParam {Dict} edit Edited content. Its sub-parameters are shown below.
    @apiParam {String} title (Sub-parameter of edit) Title of project.
    @apiParam {String} intro (Sub-parameter of edit) Introduction of project.
    @apiParam {String} background_image (Sub-parameter of edit) Static background image url. This should be preceded by a call to the upload_img/ interface to upload a background image file, with the url of the file returned by the upload_img/ interface as this parameter.
    @apiParam {Int} total_num (Sub-parameter of edit) The total number of donations expected to be received and the project ends when this number is reached.
    @apiParam {Int} start_time (Sub-parameter of edit) The time at which the project starts and before which the project will not be shown.
    @apiParam {Int} end_time (Sub-parameter of edit) The time at which the project will end. When this time is reached, the project will be closed even if it has not reached the desired number of donations.
    @apiParam {String} details (Sub-parameter of edit) Details of the project, containing rich text information.
    @apiParam {Float} price (Sub-parameter of edit) The single donation price of the project.

    @apiSuccess (Success 200 return) {Int} status Edit status (0: success, 1: not_logged_in, 2: wrong_currency_type, 3: project_not_exists, 4: not_project_owner, 5: edit_fail)

    @apiParamExample {Json} Sample Request
    {
        "pid": "22fd90badc08090a9b01606dbee18ff1",
        "currency_type": "CNY (Chinese Yuan Renminbi)",
        "edit": {
            "title": "apex",
            "intro": "apex",
            "background_image": "",
            "total_num": 80,
            "start_time": 1647440000,
            "end_time": 1678970000,
            "details": "apex",
            "price": 100
            }
     }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
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