from .functions import *
from Common.decorators import *
from User.functions import *
from django.contrib.auth.hashers import make_password, check_password

regis_action = {"send_code": 0,
                "verify_code": 1,
                "set_password": 2}

reset_password_action = {"send_code": 0,
                         "verify_code": 1,
                         "set_password": 2}

@api_logger_decorator()
@check_login_forbidden_decorator()
@check_request_method_decorator(method=["POST"])
@check_request_parameters_decorator(params=["username", "password"])
@record_login_fail_decorator()
def login(request):
    """
    @api {POST} /login/ user login
    @apiVersion 1.0.0
    @apiName login
    @apiGroup User
    @apiDescription api for user login

    @apiParam {String} username Username (mail address)
    @apiParam {String} password Password

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100004] user is already logged in, [100005] invalid username, [100006] wrong password, [400004] temporary ban due to too frequent login attempts)

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
    response_data = {"status": STATUS_CODE["success"]}
    if check_login(request):
        raise ServerError("user is already logged in")
    else:
        data = json.loads(request.body)
        mail = data["username"]
        password = data["password"]
        password = decode_password(password)
        user = DUser.get_user({"mail": mail})
        if not user:
            raise ServerError("invalid username")
        elif not check_password(password, user.password):
            raise ServerError("wrong password")
        else:
            try:
                user.update_from_fict({"last_login_time": int(time.time())})
            except ServerError as se:
                logger_standard.warning("User: {}, write last login time failed.")
            rep = HttpResponse(json.dumps(response_data), content_type="application/json")
            cookie = encode_cookie(request, user.uid, COOKIE_ENCODE_KEY)
            rep.set_signed_cookie(COOKIE_KEY, cookie, salt=COOKIE_SALT + get_request_url(request), max_age=COOKIE_EXPIRES, expires=COOKIE_EXPIRES, path=COOKIE_PATH)
            return rep

@api_logger_decorator()
@check_server_error_decorator()
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
    @apiParam {String} hide (Optional) Static avatar url. Whether the user is hiding personal information from other users. (0: no hide, 1: hide). If the user type is charity, then this field will be forced to be set to 0. Only requested if action = 2.

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100004] user is already logged in, [100007] email is already registered, [300002] email delivery failed, [300003] captcha verification failed, [300004] invalid action, [100011] invalid user type, [100012] wrong parameters for user creation, [100013] user creation failed, [300001] invalid currency type, [300006] wrong region name or code)
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
      "hide": 0
    }
    @apiSuccessExample {Json} Response-Success (action=2)
    {
        'status': 0,
        'action': 2
    }
    """
    response_data = {"status": STATUS_CODE["success"],
                     "action": "",
                     }
    if check_login(request):
        raise ServerError("user is already logged in")
    data = json.loads(request.body)
    mail = data["username"]
    action = data["action"]
    response_data["action"] = action
    if action == regis_action["send_code"]:
        if DUser.get_user({"mail": mail}):
            response_data["status"] = STATUS_CODE["email is already registered"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        code = gen_verify_code(mail, VERIFY_CODE_KEY_REGIS)
        try:
            Mail.regis_verify(mail, code, False)
        except:
            response_data["status"] = STATUS_CODE["email delivery failed"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif action == regis_action["verify_code"]:
        code = data["code"]
        if not check_verify_code(mail, VERIFY_CODE_KEY_REGIS, code):
            response_data["status"] = STATUS_CODE["captcha verification failed"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif action == regis_action["set_password"]:
        code = data["code"]
        if not check_verify_code(mail, VERIFY_CODE_KEY_REGIS, code):
            response_data["status"] = STATUS_CODE["captcha verification failed"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        create_info = {"mail": mail}
        for i in ("type", "region", "currency_type", "name", "avatar", "hide"):
            if i in data:
                create_info[i] = data[i]
        create_info["password"] = decode_password(data["password"])
        create_info["password"] = make_password(create_info["password"])
        try:
            DUser.create(create_info)
        except ServerError as se:
            response_data["status"] = se.code
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        try:
            Mail.welcome(mail, False)
        except:
            logger_standard.warning("Send welcome mail to {mail} failed.".format(mail=mail))
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data["status"] = STATUS_CODE["invalid action"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@api_logger_decorator()
@check_server_error_decorator()
@check_request_method_decorator(method=["GET"])
@get_user_decorator()
def logout(request, user):
    """
    @api {GET} /logout/ user logout
    @apiVersion 1.0.0
    @apiName logout
    @apiGroup User
    @apiDescription api for user logout

    @apiSuccess (Success 200 return) {Int} Status Status code ([0] success, [100001] user has not logged in)

    @apiSuccessExample {Json} Response-Success
    {
        'status': 0
    }
    """
    response_data = {"status": STATUS_CODE["success"]}
    rep = HttpResponse(json.dumps(response_data), content_type="application/json")
    rep.delete_cookie(COOKIE_KEY)
    return rep

@api_logger_decorator()
@check_server_error_decorator()
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

    @apiSuccess (Success 200 return) {Int} status Status code ([0] success, [100008] password setting failed, [100009] email is not registered, [100010] mismatch between logged in user and target user, [300002] email delivery failed, [300003] captcha verification failed, [300004] invalid action)
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
    response_data = {"status": STATUS_CODE["success"], "action": ""}
    data = json.loads(request.body)
    action = data["action"]
    mail = data["username"]
    response_data["action"] = action
    if user and mail != user.mail:
        response_data["status"] = STATUS_CODE["mismatch between logged in user and target user"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    user = DUser.get_user({"mail": mail})
    if not user:
        response_data["status"] = STATUS_CODE["email is not registered"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    if action == reset_password_action["send_code"]:
        code = gen_verify_code(mail, VERIFY_CODE_KEY_RESET_PASSWORD)
        try:
            Mail.reset_password_verify(mail, code, False)
        except:
            response_data["status"] = STATUS_CODE["email delivery failed"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif action == reset_password_action["verify_code"]:
        code = data["code"]
        if not check_verify_code(mail, VERIFY_CODE_KEY_RESET_PASSWORD, code):
            response_data["status"] = STATUS_CODE["captcha verification failed"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif action == reset_password_action["set_password"]:
        code = data["code"]
        if not check_verify_code(mail, VERIFY_CODE_KEY_RESET_PASSWORD, code):
            response_data["status"] = STATUS_CODE["captcha verification failed"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        try:
            user.update_from_fict({"password": make_password(decode_password(data["password"]))})
        except ServerError as se:
            raise ServerError("password setting failed")
        try:
            Mail.reset_password_success(mail, False)
        except:
            logger_standard.warning("Send reset password success mail to {mail} failed.".format(mail=mail))
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data["status"] = STATUS_CODE["invalid action"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")