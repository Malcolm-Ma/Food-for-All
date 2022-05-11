from .functions import *
from Common.decorators import *

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["GET", "POST"])
@get_user_decorator(force_login=False)
def get_user(request, user):
    """
    @api {GET} /get_user/ get user
    @apiVersion 1.0.0
    @apiName get_user
    @apiGroup User
    @apiDescription api to get information of user that already logged in

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [100014] target user does not exist)
    @apiSuccess (Success 200 return) {Dict} user_info Dict of user information. Its sub-parameters are shown below.
    @apiSuccess (Success 200 return) {String} uid (Sub-parameter of user_info) Userid
    @apiSuccess (Success 200 return) {String} mail (Sub-parameter of user_info) Mail address of user (username) (if the target user hides personal information, this field returns a value of "*")
    @apiSuccess (Success 200 return) {String} name (Sub-parameter of user_info) Name of user
    @apiSuccess (Success 200 return) {String} avatar (Sub-parameter of user_info) Static avatar url of user
    @apiSuccess (Success 200 return) {Int} type (Sub-parameter of user_info) User type (0: administrator, 1: charity, 2: guest)
    @apiSuccess (Success 200 return) {String} region (Sub-parameter of user_info) Country or region. It should be included in the list provided by "region_list/" interfac. (if the target user hides personal information, this field returns a value of "*")
    @apiSuccess (Success 200 return) {String} currency_type (Sub-parameter of user_info) Currency type. It should be included in the list provided by "currency_list/" interface. (this field is only returned if the request method is GET or if the target of the query is the user himself)
    @apiSuccess (Success 200 return) {Int} hide (Sub-parameter of user_info) Whether the user is hiding personal information from other users. (0: no hide, 1: hide). (this field is only returned if the request method is GET or if the target of the query is the user himself)
    @apiSuccess (Success 200 return) {List(String)} project (Sub-parameter of user_info) List of projects' pid. If user_type=1 then the list represents projects owned by the user. If user_type=2 then the list represents projects donated by the user. (if the target user hides personal information, this field returns a value of "*")
    @apiSuccess (Success 200 return) {Int} regis_time (Sub-parameter of user_info) Timestamp of when the user was created. It is the number of seconds that have elapsed since 0:0:0 on 1 January 1970. (this field is only returned if the request method is GET or if the target of the query is the user himself)
    @apiSuccess (Success 200 return) {Int} last_login_time (Sub-parameter of user_info) Timestamp of the last time the user logged in. It is the number of seconds that have elapsed since 0:0:0 on 1 January 1970. (this field is only returned if the request method is GET or if the target of the query is the user himself)
    @apiSuccess (Success 200 return) {Dict} donate_history (Sub-parameter of user_info) Donate history. If user_type=1, this data format is represented as {string: {string: {string: int}}}, i.e. {pid: {uid: {timestamp: num}}}. This means that user "uid" has donated "num" times to project "pid" at time "timestamp". If user_type=2, then the data format is {string: {string: int}}, i.e. {pid: {timestamp: num}}. This means that the user donated "num" times to project "pid" at time "timestamp". (if the target user hides personal information, this field returns a value of "*")
    @apiSuccess (Success 200 return) {List(String)} share_mail_history (Sub-parameter of user_info) The mails that the user has previously shared the projects to. (this field is only returned if the request method is GET or if the target of the query is the user himself)

    @apiParamExample {Json} Sample Request
    {
        "uid": ""
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "user_info": {
            "uid": "741f7803962ef9a807104839830ce0c1",
            "mail": "danielalvarez@example.com",
            "name": "Clark Inc",
            "avatar": "static/JaDTqBnJ.jpg",
            "type": 1,
            "region": "CN",
            "currency_type": "NOK",
            "hide": 0
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

    @apiParamExample {Json} Sample Request
    {
        "uid": "qwerasdfzxcv1234qwerasdfzxcv1234"
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0,
        "user_info": {
            "uid": "qwerasdfzxcv1234qwerasdfzxcv1234",
            "mail": "*",
            "name": "Clark Inc",
            "avatar": "static/JaDTqBnJ.jpg",
            "type": 2,
            "region": "*",
            "project": "*",
            "donate_history": "*"
        }
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    user_info_key = {"self": ["uid", "mail", "name", "avatar", "type", "region", "currency_type", "project", "regis_time", "last_login_time", "donate_history", "share_mail_history", "hide"],
                     "other": ["uid", "mail", "name", "avatar", "type", "region", "project", "donate_history"]}
    if request.method == "GET":
        if not user:
            raise ServerError("user has not logged in")
        else:
            response_data["user_info"] = user.to_dict(fields=user_info_key["self"])
    else:
        data = json.loads(request.body)
        uid = data["uid"]
        if not uid and not user:
            raise ServerError("user has not logged in")
        elif not uid or (user and uid == user.uid):
            response_data["user_info"] = user.to_dict(fields=user_info_key["self"])
        else:
            user = DUser.get_user({"uid": uid})
            if not user:
                raise ServerError("target user does not exist")
            response_data["user_info"] = user.to_dict(fields=user_info_key["other"], check_hide=True)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["POST"])
@get_user_decorator()
def edit_user(request, user):
    """
    @api {POST} /edit_user/ edit user
    @apiVersion 1.0.0
    @apiName edit_user
    @apiGroup User
    @apiDescription api for editing user information by user already login

    @apiParam {String} name (Optional) Name of user.
    @apiParam {String} region (Optional) Country or region of user.
    @apiParam {String} currency_type (Optional) Default currency type of user.
    @apiParam {String} avatar (Optional) Static avatar url of user. This should be preceded by a call to the upload_img/ interface to upload an avatar image file, with the url of the file returned by the upload_img/ interface as this parameter.
    @apiParam {Int} hide (Optional) Whether the user is hiding personal information from other users. (0: no hide, 1: hide) (only request if user type is charity, since charity users should not hide personal information)

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100001] user has not logged in, [100002] user update failed, [300001] invalid currency type, [300006] wrong region name or code)

    @apiParamExample {Json} Sample Request
    {
        "name": "qwer",
        "region": "Afghanistan",
        "currency_type": "AFN",
        "avatar": "/static/avatar.16475514014588146.jpg"
        "hide": 0
    }
    @apiSuccessExample {Json} Response-Success
    {
        "status": 0
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    data = json.loads(request.body)
    edit_dict = {}
    for i in ("name", "region", "currency_type", "avatar", "hide"):
        if i in data:
            edit_dict[i] = data[i]
    user.update_from_fict(edit_dict)
    return HttpResponse(json.dumps(response_data), content_type="application/json")