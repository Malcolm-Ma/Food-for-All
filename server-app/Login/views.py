from django.http import HttpResponse, HttpResponseBadRequest
import json
from Mail.functions import Mail
from .functions import *
from Logging.functions import *
from User.functions import *

@api_logger_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["username", "password"])
def login(request):
    """
    @api {POST} /login/ user login
    @apiVersion 1.0.0
    @apiName login
    @apiGroup User
    @apiDescription api for user login

    @apiParam {String} username Username (mail address)
    @apiParam {String} password Password

    @apiSuccess (Success 200 return) {Int} status Status code (0: success, 100004: user_already_logged_in, 100005: wrong_username, 100006: wrong_password)

    @apiParamExample {Json} Sample Request
    {
      "username": "531273646@qq.com",
      "password": "123456"
    }
    @apiSuccessExample {Json} Response-Success
    {
        'status': 0
    }
    """
    #if request.method != "POST":
    #    return HttpResponseBadRequest()
    response_data = {"status": ""}
    if check_login(request):
        response_data["status"] = STATUS_CODE["user_already_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        data = json.loads(request.body)
        mail = data["username"]
        password = data["password"]
        user = DUser.get_user({"mail": mail})
        if not user:
            response_data["status"] = STATUS_CODE["wrong_username"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif user.password != password:
            response_data["status"] = STATUS_CODE["wrong_password"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            user.update_from_fict({"last_login_time": int(time.time())})
            response_data["status"] = STATUS_CODE["success"]
            rep = HttpResponse(json.dumps(response_data), content_type="application/json")
            cookie = encode_cookie(request, user.uid, COOKIE_ENCODE_KEY)
            rep.set_signed_cookie(COOKIE_KEY, cookie, salt=COOKIE_SALT + get_request_url(request), max_age=COOKIE_EXPIRES, expires=COOKIE_EXPIRES, path=COOKIE_PATH)
            return rep

@api_logger_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["username", "action"])
def regis(request):
    """
    @api {POST} /regis/ user registration
    @apiVersion 1.0.0
    @apiName regis
    @apiGroup User
    @apiDescription api for user registration

    @apiParam {String} username Username (mail address)
    @apiParam {Int} action Registration action (0: send_code, 1: verify_code, 2: set_password)
    @apiParam {String} code (Optional) Registration code received by user mail. Only requested if action = 1 or 2.
    @apiParam {String} password (Optional) Password. Only requested if action = 2.
    @apiParam {Int} type (Optional) User type (1: charity, 2: guest). Only requested if action = 2.
    @apiParam {String} region (Optional) Country or region. It should be included in the list provided by "region_list/" interface. Only requested if action = 2.
    @apiParam {String} currency_type (Optional) Currency type. It should be included in the list provided by "currency_list/" interface. Only requested if action = 2.
    @apiParam {String} name (Optional) User name. Only requested if action = 2.
    @apiParam {String} avatar (Optional) Static avatar url. This should be preceded by a call to the upload_img/ interface to upload an avatar image file, with the url of the file returned by the upload_img/ interface as this parameter. Only requested if action = 2.

    @apiSuccess (Success 200 return) {Int} status Status code (0: success, 100004: user_already_logged_in, 100007: mail_already_registered, 100008: set_password_fail, 300002: mail_send_fail, 300003: code_verify_fail, 300004: wrong_action)
    @apiSuccess (Success 200 return) {Int} action Registration action (0: send_code, 1: verify_code, 2: set_password)

    @apiParamExample {Json} Sample Request (action=0)
    {
      "username": "531273646@qq.com",
      "action": 0
    }
    @apiSuccessExample {Json} Response-Success (action=0)
    {
        'status': 0,
        'action': 0
    }

    @apiParamExample {Json} Sample Request (action=1)
    {
      "username": "531273646@qq.com",
      "action": 1,
      "code": "qwe123"
    }
    @apiSuccessExample {Json} Response-Success (action=1)
    {
        'status': 0,
        'action': 1
    }

    @apiParamExample {Json} Sample Request (action=2)
    {
      "username": "531273646@qq.com",
      "action": 2,
      "password": "123456",
      "region": "CN",
      "currency_type": "GBP",
      "name": "tyl",
      "avatar": "",
      "type": 2,
      "code": "qwe123"
    }
    @apiSuccessExample {Json} Response-Success (action=2)
    {
        'status': 0,
        'action': 2
    }
    """
    #if request.method != "POST":
    #    return HttpResponseBadRequest()
    response_data = {"status": "",
                     "action": "",
                     }
    if check_login(request):
        response_data["status"] = STATUS_CODE["user_already_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    data = json.loads(request.body)
    mail = data["username"]
    action = data["action"]
    response_data["action"] = action
    if action == regis_action["send_code"]:
        if DUser.get_user({"mail": mail}):
            response_data["status"] = STATUS_CODE["mail_already_registered"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        code = gen_verify_code(mail, VERIFY_CODE_KEY_REGIS)
        try:
            Mail.regis_verify(mail, code, False)
            response_data["status"] = STATUS_CODE["success"]
        except:
            response_data["status"] = STATUS_CODE["mail_send_fail"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif action == regis_action["verify_code"]:
        code = data["code"]
        if check_verify_code(mail, VERIFY_CODE_KEY_REGIS, code):
            response_data["status"] = STATUS_CODE["success"]
        else:
            response_data["status"] = STATUS_CODE["code_verify_fail"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif action == regis_action["set_password"]:
        code = data["code"]
        if not check_verify_code(mail, VERIFY_CODE_KEY_REGIS, code):
            response_data["status"] = STATUS_CODE["code_verify_fail"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        create_info = {"mail": mail}
        for i in ("password", "type", "region", "currency_type", "name", "avatar"):
            create_info[i] = data[i]
        if not DUser.create(create_info):
            response_data["status"] = STATUS_CODE["set_password_fail"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        Mail.welcome(mail)
        response_data["status"] = STATUS_CODE["success"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data["status"] = STATUS_CODE["wrong_action"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_request_method_decorator(method=["GET"])
@get_user_decorator()
def logout(request, user):
    """
    @api {GET} /logout/ user logout
    @apiVersion 1.0.0
    @apiName logout
    @apiGroup User
    @apiDescription api for user logout

    @apiSuccess (Success 200 return) {Int} Status Status code (0: success, 100001: user_not_logged_in)

    @apiSuccessExample {Json} Response-Success
    {
        'status': 0
    }
    """
    #if request.method != "GET":
    #    return HttpResponseBadRequest()
    response_data = {"status": ""}
    #if not check_login(request):
    #    response_data["status"] = STATUS_CODE["not_logged_in"]
    #    return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data["status"] = STATUS_CODE["success"]
    rep = HttpResponse(json.dumps(response_data), content_type="application/json")
    rep.delete_cookie(COOKIE_KEY)
    return rep

@api_logger_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["username", "action"])
@get_user_decorator(force_login=False)
def reset_password(request, user):
    """
    @api {POST} /reset_password/ reset password
    @apiVersion 1.0.0
    @apiName reset_password
    @apiGroup User
    @apiDescription api to reset password

    @apiParam {String} username Username (mail address)
    @apiParam {Int} action Reset password action (0: send_code, 1: verify_code, 2: set_password)
    @apiParam {String} code (Optional) Reset password code received by user mail. Only requested if action = 1 or 2.
    @apiParam {String} password (Optional) Password. Only requested if action = 2.

    @apiSuccess (Success 200 return) {Int} status Status code (0: success, 100008: set_password_fail, 100009: mail_not_registered, 100010: user_not_match, 300002: mail_send_fail, 300003: code_verify_fail, 300004: wrong_action)
    @apiSuccess (Success 200 return) {Int} action Registration action (0: send_code, 1: verify_code, 2: set_password)

    @apiParamExample {Json} Sample Request (action=0)
    {
      "username": "531273646@qq.com",
      "action": 0
    }
    @apiSuccessExample {Json} Response-Success (action=0)
    {
        'status': 0,
        'action': 0
    }

    @apiParamExample {Json} Sample Request (action=1)
    {
      "username": "531273646@qq.com",
      "action": 1,
      "code": "qwe123"
    }
    @apiSuccessExample {Json} Response-Success (action=1)
    {
        'status': 0,
        'action': 1
    }

    @apiParamExample {Json} Sample Request (action=2)
    {
      "username": "531273646@qq.com",
      "action": 2,
      "password": "123456",
      "code": "qwe123"
    }
    @apiSuccessExample {Json} Response-Success (action=2)
    {
        'status': 0,
        'action': 2
    }
    """
    #if request.method != "POST":
    #    return HttpResponseBadRequest()
    response_data = {"status": "",
                     "action": "",
                     }
    data = json.loads(request.body)
    action = data["action"]
    mail = data["username"]
    response_data["action"] = action
    #user = check_login(request)
    if user and mail != user.mail:
        response_data["status"] = STATUS_CODE["user_not_match"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    user = DUser.get_user({"mail": mail})
    if not user:
        response_data["status"] = STATUS_CODE["mail_not_registered"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    if action == reset_password_action["send_code"]:
        code = gen_verify_code(mail, VERIFY_CODE_KEY_RESET_PASSWORD)
        try:
            Mail.reset_password_verify(mail, code, False)
            response_data["status"] = STATUS_CODE["success"]
        except:
            response_data["status"] = STATUS_CODE["mail_send_fail"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif action == reset_password_action["verify_code"]:
        code = data["code"]
        if check_verify_code(mail, VERIFY_CODE_KEY_RESET_PASSWORD, code):
            response_data["status"] = STATUS_CODE["success"]
        else:
            response_data["status"] = STATUS_CODE["code_verify_fail"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif action == reset_password_action["set_password"]:
        code = data["code"]
        if not check_verify_code(mail, VERIFY_CODE_KEY_RESET_PASSWORD, code):
            response_data["status"] = STATUS_CODE["code_verify_fail"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        update_info = {"password": data["password"]}
        if not user.update_from_fict(update_info):
            response_data["status"] = STATUS_CODE["set_password_fail"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        Mail.reset_password_success(mail)
        response_data["status"] = STATUS_CODE["success"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data["status"] = STATUS_CODE["wrong_action"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")