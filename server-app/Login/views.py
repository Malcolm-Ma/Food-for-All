from django.http import HttpResponse, HttpResponseBadRequest
import json
from Mail.functions import Mail
from .functions import *

def login(request):
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {"status": login_status["wrong_username"]}
    if check_login(request):
        response_data["status"] = login_status["already_login"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        data = json.loads(request.body)
        mail = data["username"]
        password = data["password"]
        user = get_user({"mail": mail})
        if not user:
            response_data["status"] = login_status["wrong_username"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif user.password != password:
            response_data["status"] = login_status["wrong_password"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            update_user(user, {"last_login_time": int(time.time())})
            response_data["status"] = login_status["success"]
            rep = HttpResponse(json.dumps(response_data), content_type="application/json")
            cookie = encode_cookie(request, user.uid)
            rep.set_signed_cookie(COOKIE_KEY, cookie, salt=COOKIE_SALT, max_age=COOKIE_EXPIRES, expires=COOKIE_EXPIRES, path=COOKIE_PATH)
            return rep

def regis(request):
    if request.method != "POST":
        return HttpResponseBadRequest()
    response_data = {"status": "",
                     "action": "",
                     }
    if check_login(request):
        response_data["status"] = regis_status["already_login"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        data = json.loads(request.body)
        mail = data["username"]
        action = data["action"]
        response_data["action"] = action
        if action == regis_action["send_code"]:
            if get_user({"mail": mail}):
                response_data["status"] = regis_status["mail_registed"]
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            code = gen_verify_code(mail, "regist")
            try:
                Mail.regis_verify(mail, code, False)
                response_data["status"] = regis_status["mail_send_success"]
            except:
                response_data["status"] = regis_status["mail_send_fail"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif action == regis_action["verify_code"]:
            code = data["code"]
            if check_verify_code(mail, "regist", code):
                response_data["status"] = regis_status["code_verify_success"]
            else:
                response_data["status"] = regis_status["code_verify_fail"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif action == regis_action["set_password"]:
            create_info = {"mail": mail}
            for i in ("password", "type", "region", "currency_type", "name", "avatar"):
                create_info[i] = data[i]
            if not create_user(create_info):
                response_data["status"] = regis_status["set_password_fail"]
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            Mail.welcome(mail)
            response_data["status"] = regis_status["set_password_success"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")

def logout(request):
    response_data = {"status": logout_status["not_logged_in"]}
    if not check_login(request):
        response_data["status"] = logout_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data["status"] = logout_status["success"]
    rep = HttpResponse(json.dumps(response_data), content_type="application/json")
    rep.delete_cookie(COOKIE_KEY)
    return rep