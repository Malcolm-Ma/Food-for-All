from django.http import HttpResponse, HttpResponseBadRequest
import json
from Login.functions import check_login
from .functions import *
from Project.functions import get_all_projects
from Common.decorators import *

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["GET"])
@get_user_decorator()
def get_user_info(request, user):
    """
    @api {GET} /get_user_info/ get user information
    @apiVersion 1.0.0
    @apiName get_user_info
    @apiGroup User
    @apiDescription api to get information of user that already logged in

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user_not_logged_in)
    @apiSuccess (Success 200 return) {Dict} user_info Dict of user information. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} uid (Sub-parameter of user_info) Userid
    @apiSuccess (Success 200 return) {String} mail (Sub-parameter of user_info) Mail address of user (username)
    @apiSuccess (Success 200 return) {String} name (Sub-parameter of user_info) Name of user
    @apiSuccess (Success 200 return) {String} avatar (Sub-parameter of user_info) Static avatar url of user
    @apiSuccess (Success 200 return) {Int} type (Sub-parameter of user_info) User type (0: administrator, 1: charity, 2: guest)
    @apiSuccess (Success 200 return) {String} region (Sub-parameter of user_info) Country or region. It should be included in the list provided by "region_list/" interface
    @apiSuccess (Success 200 return) {String} currency_type (Sub-parameter of user_info) Currency type. It should be included in the list provided by "currency_list/" interface
    @apiSuccess (Success 200 return) {List(String)} project (Sub-parameter of user_info) List of projects' pid. If user_type=1 then the list represents projects owned by the user. If user_type=2 then the list represents projects donated by the user.
    @apiSuccess (Success 200 return) {Int} regis_time (Sub-parameter of user_info) Timestamp of when the user was created. It is the number of seconds that have elapsed since 0:0:0 on 1 January 1970.
    @apiSuccess (Success 200 return) {Int} last_login_time (Sub-parameter of user_info) Timestamp of the last time the user logged in. It is the number of seconds that have elapsed since 0:0:0 on 1 January 1970.
    @apiSuccess (Success 200 return) {Dict} donate_history (Sub-parameter of user_info) Donate history. If user_type=1, this data format is represented as {string: {string: {string: int}}}, i.e. {pid: {uid: {timestamp: num}}}. This means that user "uid" has donated "num" times to project "pid" at time "timestamp". If user_type=2, then the data format is {string: {string: int}}, i.e. {pid: {timestamp: num}}. This means that the user donated "num" times to project "pid" at time "timestamp".
    @apiSuccess (Success 200 return) {List(String)} share_mail_history (Sub-parameter of user_info) The mails that the user has previously shared the projects to.

    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "user_info": {
            "uid": "741f7803962ef9a807104839830ce0c1",
            "mail": "danielalvarez@example.com",
            "name": "Clark Inc",
            "avatar": "static/JaDTqBnJ.jpg",
            "type": 1,
            "region": "China, Hong Kong S.A.R.",
            "currency_type": "NOK",
            "project": [
                "20176b903abc3ee64aea2c05abef294a",
                "3d34d2219e7dd9fe59b4bd7223c0faf1",
                "feafb396a267c2c9300b0f0074719c09",
                "9cf8d7ffc051e0dd471a1b0ae84e7580",
                "20b0187e0bb612e6252e3a2326ead87c",
                "22c04157e6c7b3b86050c5335bf49556"
            ],
            "regis_time": 1643460482,
            "last_login_time": 1647892237,
            "donate_history": {
                "20176b903abc3ee64aea2c05abef294a": {
                    "b83d5dcd6a6d55613b5000588e56fc66": {
                        "1644166762": 1,
                        "1644747477": 1,
                        "1645200177": 1,
                        "1645551546": 2,
                        "1646536007": 1
                    }
                }
            },
            "share_mail_history": [
                "gberry@example.com",
                "ashleymerritt@example.org"
            ]
        }
    }
    """
    #if request.method != "GET":
    #    return HttpResponseBadRequest()
    response_data = {"status": STATUS_CODE["success"],
                     "user_info": {"uid": "",
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
                                   "share_mail_history": ","}}
    #user = check_login(request)
    #if user:
    response_data["user_info"] = user.to_dict(fields=list(response_data["user_info"].keys()))
    #for i in response_data["user_info"]:
    #    response_data["user_info"][i] = user.__getattribute__(i)
    #response_data["user_info"]["region"] = RID2REGION[response_data["user_info"]["region"]]
    #response_data["user_info"]["project"] = eval(response_data["user_info"]["project"])
    #response_data["user_info"]["donate_history"] = eval(response_data["user_info"]["donate_history"])
    #response_data["user_info"]["share_mail_history"] = eval(response_data["user_info"]["share_mail_history"])
    #response_data["status"] = STATUS_CODE["success"]
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["name", "region", "currency_type", "avatar"])
@get_user_decorator()
def edit_user(request, user):
    """
    @api {POST} /edit_user/ edit user
    @apiVersion 1.0.0
    @apiName edit_user
    @apiGroup User
    @apiDescription api for editing user information by user already login

    @apiParam {String} name Name of user.
    @apiParam {String} region Country or region of user.
    @apiParam {String} currency_type Default currency type of user.
    @apiParam {String} avatar Static avatar url of user. This should be preceded by a call to the upload_img/ interface to upload an avatar image file, with the url of the file returned by the upload_img/ interface as this parameter.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user_not_logged_in, [100002] edit_user_info_fail, [300001] wrong_currency_type, [300006] wrong region name or code)

    @apiParamExample {Json} Sample Request
    {
        "name": "qwer",
        "region": "Afghanistan",
        "currency_type": "AFN",
        "avatar": "/static/avatar.16475514014588146.jpg"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    #if request.method != "POST":
    #    return HttpResponseBadRequest()
    response_data = {"status": STATUS_CODE["success"]}
    #user = check_login(request)
    #if not user:
    #    response_data["status"] = STATUS_CODE["user_not_logged_in"]
    #    return HttpResponse(json.dumps(response_data), content_type="application/json")
    data = json.loads(request.body)
    edit_dict = {}
    for i in ("name", "region", "currency_type", "avatar"):
        if i in data:
            edit_dict[i] = data[i]
    user.update_from_fict(edit_dict)
    return HttpResponse(json.dumps(response_data), content_type="application/json")