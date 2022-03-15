from django.http import HttpResponse
import json
from Mail.views import Mail
from .functions import *

def login(request):
    response_data = {"status": login_status["wrong_username"]}
    if check_login(request):
        response_data["status"] = login_status["already_login"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == "GET":
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == "POST":
        data = json.loads(request.body)
        mail = data["username"]
        password = data["password"]
        user_info = filter_user_info({"mail": mail}).first()
        if not user_info:
            response_data["status"] = login_status["wrong_username"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif user_info.password != password:
            response_data["status"] = login_status["wrong_password"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            update_user_info(filter_user_info({"mail": mail}), {"last_login_time": int(time.time())})
            response_data["status"] = login_status["success"]
            rep = HttpResponse(json.dumps(response_data), content_type="application/json")
            cookie = encode_cookie(request, user_info.uid)
            rep.set_signed_cookie("apex", cookie, salt=COOKIE_SALT, max_age=COOKIE_EXPIRES, expires=COOKIE_EXPIRES, path=COOKIE_PATH)
            return rep

def regis(request):
    response_data = {"status": "",
                     "action": "",
                     }
    if check_login(request):
        response_data["status"] = regis_status["already_login"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == "GET":
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == "POST":
        data = json.loads(request.body)
        mail = data["username"]
        action = data["action"]
        response_data["action"] = action
        if action == regis_action["send_code"]:
            if filter_user_info({"mail": mail}).first():
                response_data["status"] = regis_status["mail_registed"]
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            code = gen_regis_code(mail)
            try:
                Mail.regis_verify(mail, code)
                response_data["status"] = regis_status["mail_send_success"]
            except:
                response_data["status"] = regis_status["mail_send_fail"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif action == regis_action["verify_code"]:
            code = data["code"]
            if check_regis_code(mail, code):
                response_data["status"] = regis_status["code_verify_success"]
            else:
                response_data["status"] = regis_status["code_verify_fail"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif action == regis_action["set_password"]:
            password = data["password"]
            type = data["type"]
            region = data["region"]
            currency_type = data["currency_type"]
            name = data["name"]
            avatar = data["avatar"]
            if avatar == "" or not os.path.isfile(os.path.join(BASE_DIR, avatar)):
                avatar = DEFAULT_AVATAR
            user_info = create_user(mail, password, type, region, currency_type, name=name, avatar=avatar)
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
    rep.delete_cookie("apex")
    return rep