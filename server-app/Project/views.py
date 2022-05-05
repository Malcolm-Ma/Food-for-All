from .functions import *
from Common.decorators import *

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST", "GET"])
@get_user_decorator(force_login=False)
def get_projects_list(request, user):
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

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [200015] project order invalid , [300001] invalid currency type)
    @apiSuccess (Success 200 return) {Dict} project_info Projects list. The keys of this dictionary are the order of the projects counting from 0 and the values are the information of the projects corresponding to their order. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} pid (Sub-parameter of project_info) Pid of the project.
    @apiSuccess (Success 200 return) {String} title (Sub-parameter of project_info) Title of project.
    @apiSuccess (Success 200 return) {String} intro (Sub-parameter of project_info) Introduction of project.
    @apiSuccess (Success 200 return) {String} region (Sub-parameter of project_info) Country or region of the project's owner. It should be included in the list provided by "region_list/" interface.
    @apiSuccess (Success 200 return) {String} charity (Sub-parameter of project_info) Name of the project's owner.
    @apiSuccess (Success 200 return) {String} charity_avatar (Sub-parameter of project_info) Static avatar url of the project's owner.
    @apiSuccess (Success 200 return) {String} background_image (Sub-parameter of project_info) Static background image url of the project.
    @apiSuccess (Success 200 return) {Int} status (Sub-parameter of project_info) Status of th project (0: prepare, 1: ongoing, 2: finish).
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
        "currency_type": "CNY",
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
        "status": 0,
        "project_info": {
            "0": {
                "pid": "d48b0eac410514a8b032fd41bd20c1dc",
                "uid": "qweradsfqewradsfqweqeqewacvcdfer",
                "title": "3",
                "intro": "qwer3",
                "region": "CN",
                "charity": "3",
                "charity_avatar": "",
                "background_image": "",
                "status": 1,
                "price": 24.7987350414,
                "current_num": 3,
                "total_num": 100,
                "start_time": 1647558799,
                "end_time": 1679094899
            },
            "1": {
                "pid": "9dfd14feba9c9822377262fdf76e2c1c",
                "uid": "qweradsfqewradsfqweqeqewacvcdfer",
                "title": "13",
                "intro": "qwer13",
                "region": "CN",
                "charity": "13",
                "charity_avatar": "",
                "background_image": "",
                "status": 1,
                "price": 107.4611851794,
                "current_num": 13,
                "total_num": 100,
                "start_time": 1647558809,
                "end_time": 1679094909
            },
            "2": {
                "pid": "3494c5b8f941afb1a228260861d9f7d9",
                "uid": "qweradsfqewradsfqweqeqewacvcdfer",
                "title": "23",
                "intro": "23",
                "region": "CN",
                "charity": "23qwer",
                "charity_avatar": "",
                "background_image": "",
                "status": 1,
                "price": 190.12363531740002,
                "current_num": 23,
                "total_num": 100,
                "start_time": 1647558819,
                "end_time": 1679094919
            },
            "3": {
                "pid": "31f0b2737b1249ce207ff64eba63cb47",
                "uid": "qweradsfqewradsfqweqeqewacvcdfer",
                "title": "30",
                "intro": "30qwer",
                "region": "CN",
                "charity": "30",
                "charity_avatar": "",
                "background_image": "",
                "status": 1,
                "price": 247.98735041400002,
                "current_num": 30,
                "total_num": 100,
                "start_time": 1647558826,
                "end_time": 1679094926
            },
            "4": {
                "pid": "8dcad1d3db4dc77241eecc82a9310a73",
                "uid": "qweradsfqewradsfqweqeqewacvcdfer",
                "title": "31qwer",
                "intro": "31",
                "region": "CN",
                "charity": "31",
                "charity_avatar": "",
                "background_image": "",
                "status": 1,
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
        "currency_type": "CNY",
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
    response_data = {"status": STATUS_CODE["success"],
                     "project_info": {},
                     "page_info": {"page": 1,
                                   "page_size": 1,
                                   "total_page": 1},
                     "currency_type": "GBP",
                     "order": {"current_order": "",
                               "order_list": DProjectQuery.order_list},
                     "search": "",
                     "valid_only": 1}
    if request.method == "GET":
        page_size = 20
        order = "-start_time"
        current_page = 1
        search = ""
        uid = ""
        valid_only = 1
        currency_type = "GBP"
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
    if user and not currency_type:
        currency_type = user.currency_type
    pq = DProjectQuery()
    pq.get_ready(uid=uid, valid_only=valid_only)
    projects_dict, batch_num = pq.filter(current_page, page_size, order, search, currency_type,
                                         fields=("pid", "uid", "title", "intro", "region",
                                                 "charity", "charity_avatar", "background_image", "price",
                                                 "current_num", "total_num", "start_time", "end_time", "status"))
    response_data["search"] = search
    response_data["valid_only"] = valid_only
    response_data["currency_type"] = currency_type
    response_data["page_info"]["page"] = current_page
    response_data["page_info"]["page_size"] = page_size
    response_data["page_info"]["total_page"] = batch_num
    response_data["project_info"] = projects_dict
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["pid", "currency_type"])
@get_project_decorator()
def get_project(request, project):
    """
    @api {POST} /get_project/ get project
    @apiVersion 1.0.0
    @apiName get_project
    @apiGroup Project
    @apiDescription api to get project details

    @apiParam {String} pid Pid of the project.
    @apiParam {String} currency_type Currency type. It should be included in the list provided by "currency_list/" interface.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [200002] project does not exist, [300001] invalid currency type)
    @apiSuccess (Success 200 return) {Dict} project_info Dict of project information. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} pid (Sub-parameter of project_info) Pid of the project.
    @apiSuccess (Success 200 return) {String} uid (Sub-parameter of project_info) Uid of the project's owner.
    @apiSuccess (Success 200 return) {String} title (Sub-parameter of project_info) Title of project.
    @apiSuccess (Success 200 return) {String} intro (Sub-parameter of project_info) Introduction of project.
    @apiSuccess (Success 200 return) {String} region (Sub-parameter of project_info) Country or region of the project's owner. It should be included in the list provided by "region_list/" interface.
    @apiSuccess (Success 200 return) {String} charity (Sub-parameter of project_info) Name of the project's owner.
    @apiSuccess (Success 200 return) {String} charity_avatar (Sub-parameter of project_info) Static avatar url of the project's owner.
    @apiSuccess (Success 200 return) {String} background_image (Sub-parameter of project_info) Static background image url of the project.
    @apiSuccess (Success 200 return) {Int} status (Sub-parameter of project_info) Status of the project (0: prepare, 1: ongoing, 2: finish).
    @apiSuccess (Success 200 return) {String} details (Sub-parameter of project_info) Details of the project, containing rich text information.
    @apiSuccess (Success 200 return) {Float} price (Sub-parameter of project_info) The single donation price of the project.
    @apiSuccess (Success 200 return) {Dict} donate_history (Sub-parameter of project_info) Donate history. The data format is {string: {string: int}}, i.e. {uid: {timestamp: num}}. This means that the user "uid" donated "num" times to the project at time "timestamp".
    @apiSuccess (Success 200 return) {Int} current_num (Sub-parameter of project_info) Number of donations accepted.
    @apiSuccess (Success 200 return) {Int} total_num (Sub-parameter of project_info) The total number of donations expected to be received and the project ends when this number is reached.
    @apiSuccess (Success 200 return) {Int} start_time (Sub-parameter of project_info) The time at which the project starts and before which the project will not be shown.
    @apiSuccess (Success 200 return) {Int} end_time (Sub-parameter of project_info) The time at which the project will end. When this time is reached, the project will be closed even if it has not reached the desired number of donations.

    @apiParamExample {Json} Sample Request
    {
        "pid": "360a27773752a7a025b3cd3d931f26e2",
        "currency_type": "CNY"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "project_info": {
            "pid": "360a27773752a7a025b3cd3d931f26e2",
            "uid": "506d201c0d8d23fcee2a4bada084acae",
            "title": "49",
            "intro": "49",
            "region": "Turkey",
            "charity": "qwer",
            "charity_avatar": "",
            "background_image": "",
            "status": 1,
            "details": "49",
            "price": 63.8893964219,
            "donate_history": {},
            "current_num": 49,
            "total_num": 100,
            "start_time": 1647549001,
            "end_time": 1679085101
        }
    }
    """
    response_data = {"status": STATUS_CODE["success"], "project_info": ""}
    data = json.loads(request.body)
    currency_type = data["currency_type"]
    response_data["project_info"] = project.to_dict(currency_type=currency_type)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["GET"])
@get_user_decorator()
def create_project(request, user):
    """
    @api {GET} /create_project/ create project
    @apiVersion 1.0.0
    @apiName create_project
    @apiGroup Project
    @apiDescription api for creating project by charity user

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [100003] operation is not available to individual user, [200001] project creation failed)
    @apiSuccess (Success 200 return) {String} pid Pid of the project just created.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "pid": "fa00cb5f2e648afa9a39d99098c4fc84"
    }
    """
    response_data = {"status": STATUS_CODE["success"], "pid": ""}
    pid = user.create_project()
    response_data["pid"] = pid
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["pid"])
@get_user_decorator()
@get_project_decorator()
def delete_project(request, user, project):
    """
    @api {POST} /delete_project/ delete project
    @apiVersion 1.0.0
    @apiName delete_project
    @apiGroup Project
    @apiDescription api to delete project by its owner

    @apiParam {String} pid Pid of the project.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project, [200004] project is not deletable)

    @apiParamExample {Json} Sample Request
    {
        "pid": "b42fcd36aac47bfafdd6b7a543c55c30"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    user.delete_project(project)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["pid", "currency_type", "edit"])
@get_user_decorator()
@get_project_decorator()
def edit_project(request, user, project):
    """
    @api {POST} /edit_project/ edit project
    @apiVersion 1.0.0
    @apiName edit_project
    @apiGroup Project
    @apiDescription api for editing project information by its owner

    @apiParam {String} pid Pid of the project.
    @apiParam {String} currency_type Currency type. It should be included in the list provided by "currency_list/" interface.
    @apiParam {Dict} edit Edited content. Its sub-parameters are shown below.
    @apiParam {String} title (Sub-parameter of edit) Title of project.
    @apiParam {String} intro (Sub-parameter of edit) Introduction of project.
    @apiParam {String} background_image (Sub-parameter of edit) Static background image url. This should be preceded by a call to the upload_img/ interface to upload a background image file, with the url of the file returned by the upload_img/ interface as this parameter.
    @apiParam {Int} total_num (Sub-parameter of edit) The total number of donations expected to be received and the project ends when this number is reached.
    @apiParam {Int} end_time (Sub-parameter of edit) The time at which the project will end. When this time is reached, the project will be closed even if it has not reached the desired number of donations.
    @apiParam {String} details (Sub-parameter of edit) Details of the project, containing rich text information.
    @apiParam {Float} price (Sub-parameter of edit) The single donation price of the project.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project, [200005] project update failed, [200006] project is not editable, [200012] project end time is invalid, [200014] project price invalid, [300001] invalid currency type)

    @apiParamExample {Json} Sample Request
    {
        "pid": "22fd90badc08090a9b01606dbee18ff1",
        "currency_type": "CNY",
        "edit": {
            "title": "apex",
            "intro": "apex",
            "background_image": "",
            "total_num": 80,
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
    response_data = {"status": STATUS_CODE["success"]}
    data = json.loads(request.body)
    currency_type = data["currency_type"]
    if project.uid != user.uid:
        raise ServerError("user is not the owner of the project")
    if project.status != PROJECT_STATUS["prepare"]:
        raise ServerError("project is not editable")
    edit_dict = {}
    for i in ("title", "intro", "background_image", "total_num", "end_time", "details", "price"):
        if i in data["edit"]:
            edit_dict[i] = data["edit"][i]
    if "price" in edit_dict:
        cid = currency2cid(currency_type)
        if not cid:
            raise ServerError("invalid currency type")
        edit_dict["price"] = edit_dict["price"] / EXCHANGE_RATE[cid]
    project.update_from_fict(edit_dict)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["pid"])
@get_user_decorator()
@get_project_decorator()
def start_project(request, user, project):
    """
    @api {POST} /start_project/ start project
    @apiVersion 1.0.0
    @apiName start_project
    @apiGroup Project
    @apiDescription api to start a prepared or suspended project

    @apiParam {String} pid Pid of the project.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project, [200007] project information is incomplete, [200008] project start up failed, [200009] project has already started, [200016] project is aiready finished, [500001] create paypal product failed)

    @apiParamExample {Json} Sample Request
    {
        "pid": "22fd90badc08090a9b01606dbee18ff1"
     }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    user.start_project(project)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["pid"])
@get_user_decorator()
@get_project_decorator()
def suspend_project(request, user, project):
    """
    @api {POST} /suspend_project/ suspend project
    @apiVersion 1.0.0
    @apiName suspend_project
    @apiGroup Project
    @apiDescription api to suspend an ongoing project

    @apiParam {String} pid Pid of the project.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, 100001: user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project, [200016] project is aiready finished, [200017] project is not ongoing, [200018] project suspension failed)

    @apiParamExample {Json} Sample Request
    {
        "pid": "22fd90badc08090a9b01606dbee18ff1"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    user.suspend_project(project)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["pid"])
@get_user_decorator()
@get_project_decorator()
def stop_project(request, user, project):
    """
    @api {POST} /stop_project/ stop project
    @apiVersion 1.0.0
    @apiName stop_project
    @apiGroup Project
    @apiDescription api to stop an ongoing or suspended project

    @apiParam {String} pid Pid of the project.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, 100001: user has not logged in, [200002] project does not exist, [200003] user is not the owner of the project, [200010] project stop failed, [200011] project is not ongoing or on hold, [200016] project is aiready finished)

    @apiParamExample {Json} Sample Request
    {
        "pid": "22fd90badc08090a9b01606dbee18ff1"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    user.stop_project(project)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["GET", "POST"])
@get_user_decorator()
def get_prepare_projects_list(request, user):
    """
    @api {GET, POST} /get_prepare_projects_list/ get prepare projects list
    @apiVersion 1.0.0
    @apiName get_prepare_projects_list
    @apiGroup Project
    @apiDescription api to get projects list with status = prepare by conditions

    @apiParam {String} currency_type Currency type. It should be included in the list provided by "currency_list/" interface.
    @apiParam {Dict} page_info Information of pages. Its sub-parameters are shown below.
    @apiParam {Int} page_size (Sub-parameter of page_info) Number of projects displayed per page.
    @apiParam {Int} page (Sub-parameter of page_info) Current page number.
    @apiParam {String} search The string to be retrieved. It should be set to "" when the search action has not occurred.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [100003] operation is not available to individual user, [300001] invalid currency type)
    @apiSuccess (Success 200 return) {Dict} project_info Projects list. The keys of this dictionary are the order of the projects counting from 0 and the values are the information of the projects corresponding to their order. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} pid (Sub-parameter of project_info) Pid of the project.
    @apiSuccess (Success 200 return) {String} title (Sub-parameter of project_info) Title of project.
    @apiSuccess (Success 200 return) {String} intro (Sub-parameter of project_info) Introduction of project.
    @apiSuccess (Success 200 return) {String} region (Sub-parameter of project_info) Country or region of the project's owner. It should be included in the list provided by "region_list/" interface.
    @apiSuccess (Success 200 return) {String} charity (Sub-parameter of project_info) Name of the project's owner.
    @apiSuccess (Success 200 return) {String} charity_avatar (Sub-parameter of project_info) Static avatar url of the project's owner.
    @apiSuccess (Success 200 return) {String} background_image (Sub-parameter of project_info) Static background image url of the project.
    @apiSuccess (Success 200 return) {Int} status (Sub-parameter of project_info) Status of th project (0: prepare, 1: ongoing, 2: finish).
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
    @apiSuccess (Success 200 return) {String} search The string has been retrieved. It would be set to "" when the search action has not occurred.

    @apiParamExample {Json} Sample Request
    {
        "currency_type": "CNY",
        "page_info": {
                "page_size": 3,
                "page": 1
                },
        "search": "qwer",
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "project_info": {
            "0": {
                "pid": "d48b0eac410514a8b032fd41bd20c1dc",
                "uid": "qweradsfqewradsfqweqeqewacvcdfer",
                "title": "3",
                "intro": "qwer3",
                "region": "CN",
                "charity": "3",
                "charity_avatar": "",
                "background_image": "",
                "status": 0,
                "price": 24.7987350414,
                "current_num": 0,
                "total_num": 100,
                "start_time": 0,
                "end_time": 1679094899
            },
            "1": {
                "pid": "9dfd14feba9c9822377262fdf76e2c1c",
                "uid": "qweradsfqewradsfqweqeqewacvcdfer",
                "title": "13",
                "intro": "qwer13",
                "region": "CN",
                "charity": "3",
                "charity_avatar": "",
                "background_image": "",
                "status": 0,
                "price": 107.4611851794,
                "current_num": 0,
                "total_num": 100,
                "start_time": 0,
                "end_time": 1679094909
            },
            "2": {
                "pid": "3494c5b8f941afb1a228260861d9f7d9",
                "uid": "qweradsfqewradsfqweqeqewacvcdfer",
                "title": "23",
                "intro": "23",
                "region": "CN",
                "charity": "3",
                "charity_avatar": "",
                "background_image": "",
                "status": 0,
                "price": 190.12363531740002,
                "current_num": 0,
                "total_num": 100,
                "start_time": 0,
                "end_time": 1679094919
            }
        },
        "page_info": {
            "page": 1,
            "page_size": 3,
            "total_page": 2
        },
        "currency_type": "CNY",
        "search": "qwer"
    }
    """
    response_data = {"status": STATUS_CODE["success"],
                     "project_info": {},
                     "page_info": {"page": 1,
                                   "page_size": 1,
                                   "total_page": 1},
                     "currency_type": "GBP",
                     "search": ""}
    if user.type != USER_TYPE["charity"]:
        raise ServerError("operation is not available to individual user")
    if request.method == "GET":
        search = ""
        page_size = 20
        current_page = 1
        currency_type = user.currency_type
        order = "title"
    elif request.method == "POST":
        data = json.loads(request.body)
        search = data["search"]
        page_size = data["page_info"]["page_size"] if data["page_info"]["page_size"] else 20
        current_page = data["page_info"]["page"] if data["page_info"]["page"] else 1
        currency_type = data["currency_type"]
        order = "title"
    pq = DProjectQuery()
    pq.get_prepare(user.uid)
    projects_dict, batch_num = pq.filter(current_page, page_size, order, search, currency_type, fields=("pid", "uid", "title", "intro", "region",
                                             "charity", "charity_avatar", "background_image", "price",
                                             "current_num", "total_num", "start_time", "end_time", "status"))
    response_data["search"] = search
    response_data["currency_type"] = currency2cid(currency_type)
    response_data["page_info"]["page"] = current_page
    response_data["page_info"]["page_size"] = page_size
    response_data["page_info"]["total_page"] = batch_num
    response_data["project_info"] = projects_dict
    return HttpResponse(json.dumps(response_data), content_type="application/json")