from django.http import HttpResponse, HttpResponseBadRequest
import json
from Login.functions import check_login
from .functions import *
from Project.functions import get_project, get_all_projects

@api_logger(logger=logger_standard)
def get_user_info(request):
    """
    @api {GET} /get_user_info/ get user information
    @apiVersion 1.0.0
    @apiName get_user_info
    @apiGroup User
    @apiDescription api to get information of user that already logged in

    @apiSuccess (Success 200 return) {String} uid Userid
    @apiSuccess (Success 200 return) {String} mail Mail address of user (username)
    @apiSuccess (Success 200 return) {String} name Name of user
    @apiSuccess (Success 200 return) {String} avatar Static avatar url of user
    @apiSuccess (Success 200 return) {Int} type User type (0: administrator, 1: charity, 2: guest)
    @apiSuccess (Success 200 return) {String} region Country or region. It should be included in the list provided by "region_list/" interface
    @apiSuccess (Success 200 return) {String} currency_type Currency type. It should be included in the list provided by "currency_list/" interface
    @apiSuccess (Success 200 return) {List(String)} project List of projects' pid. If user_type=1 then the list represents projects owned by the user. If user_type=2 then the list represents projects donated by the user.
    @apiSuccess (Success 200 return) {Int} regis_time Timestamp of when the user was created. It is the number of seconds that have elapsed since 0:0:0 on 1 January 1970.
    @apiSuccess (Success 200 return) {Int} last_login_time Timestamp of the last time the user logged in. It is the number of seconds that have elapsed since 0:0:0 on 1 January 1970.
    @apiSuccess (Success 200 return) {Dict} donate_history Donate history. If user_type=1, this data format is represented as {string: {string: {string: int}}}, i.e. {pid: {uid: {timestamp: num}}}. This means that user "uid" has donated "num" times to project "pid" at time "timestamp". If user_type=2, then the data format is {string: {string: int}}, i.e. {pid: {timestamp: num}}. This means that the user donated "num" times to project "pid" at time "timestamp".
    @apiSuccess (Success 200 return) {List(String)} share_mail_history The mails that the user has previously shared the projects to.

    @apiSuccessExample {Json} Response-Success
    {
        "uid": "ef0df32de0f9c6848448c1c9e488b982",
        "mail": "ty_liang@foxmail.com",
        "name": "asdfqwer",
        "avatar": "",
        "type": 1,
        "region": "United Kingdom",
        "currency_type": "GBP",
        "project": ['d5d6e370fa077b75e786708c7b6f3a2e', 'd5d6e370fa077b75e786708c7b6f3a43', ...],
        "regis_time": 1647441269,
        "last_login_time": 1647547074,
        "donate_history": {'d5d6e370fa077b75e786708c7b6f3a2e': {'1647547079': 3,
                                                                '1647547179': 1},
                           'd5d6e370fa077b75e786708c7b6f3a43': {'1647547049': 1,
                                                                '1647547333': 1},
                           ...
                           },
        "share_mail_history": ["531273646@qq.com"]
    }
    """
    if request.method != "GET":
        return HttpResponseBadRequest()
    response_data = {"uid": "",
                     "mail": "",
                     "name": "",
                     "avatar": "",
                     "type": "",
                     "region": "",
                     "currency_type": "",
                     "project": "[]",
                     "regis_time": 0,
                     "last_login_time": 0,
                     "donate_history": "{}",
                     "share_mail_history": ","}
    user = check_login(request)
    if user:
        for i in response_data:
            response_data[i] = user.__getattribute__(i)
        response_data["region"] = RID2REGION[response_data["region"]]
        response_data["project"] = eval(response_data["project"])
        response_data["donate_history"] = eval(response_data["donate_history"])
        response_data["share_mail_history"] = eval(response_data["share_mail_history"])
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger(logger=logger_standard)
def edit_user_info(request):
    """
    @api {POST} /edit_user_info/ edit user information
    @apiVersion 1.0.0
    @apiName edit_user_info
    @apiGroup User
    @apiDescription api for editing user information by user already login

    @apiParam {String} name Name of user.
    @apiParam {String} region Country or region of user.
    @apiParam {String} currency_type Default currency type of user.
    @apiParam {String} avatar Static avatar url of user. This should be preceded by a call to the upload_img/ interface to upload an avatar image file, with the url of the file returned by the upload_img/ interface as this parameter.

    @apiSuccess (Success 200 return) {Int} status Edit status (0: success, 1: not_logged_in, 2: edit_fail)

    @apiParamExample {Json} Sample Request
    {
        "name": "qwer",
        "region": "Afghanistan",
        "currency_type": "AFN (Afghan Afghani)",
        "avatar": "/static/avatar.16475514014588146.jpg"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {"status": edit_user_info_status["edit_fail"]}
    user = check_login(request)
    if not user:
        response_data["status"] = edit_user_info_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    data = json.loads(request.body)
    edit_dict = {}
    for i in ("name", "region", "currency_type", "avatar"):
        if i in data:
            edit_dict[i] = data[i]
    if not update_user(user, edit_dict):
        response_data["status"] = edit_user_info_status["edit_fail"]
    else:
        if user.type == USER_TYPE["charity"]:
            edit_dict = {}
            if "name" in data:
                edit_dict["charity"] = data["name"]
            if "avatar" in data:
                edit_dict["charity_avatar"] = data["avatar"]
            if "region" in data:
                edit_dict["region"] = data["region"]
            if edit_dict:
                projects = get_all_projects(user.uid)
                projects.update(**edit_dict)
        response_data["status"] = edit_user_info_status["success"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")