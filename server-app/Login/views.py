#from django.shortcuts import render, redirect
from django.http import HttpResponse
from DataBase import models
from FoodForAll.settings import COOKIE_EXPIRES, COOKIE_PATH, COOKIE_SALT, REGIS_CODE_EXPIRES, DEFAULT_AVATAR
from Mail.views import Mail
import time
from hashlib import md5
import json

login_status = {"success": 0,
                "already_login": 1,
                "wrong_username": 2,
                "wrong_password": 3,}

regis_status = {"mail_registed": 0,
                "already_login": 1,
                "mail_send_success": 2,
                "mail_send_fail": 3,
                "code_verify_success": 4,
                "code_verify_fail": 5,
                "set_password_success": 6}

regis_action = {"send_code": 0,
                "verify_code": 1,
                "set_password": 2}

logout_status = {"success": 0,
                 "not_logged_in": 1}

# Create your views here.
def gen_regis_code(mail, expires=REGIS_CODE_EXPIRES, if_check=False):
    dynamic_num = int(time.time()) // expires
    code1 = md5((str(dynamic_num) + mail).encode("utf-8")).hexdigest()[:6]
    if not if_check:
        return code1
    code2 = md5((str(dynamic_num - 1) + mail).encode("utf-8")).hexdigest()[:6]
    return code1, code2

def check_regis_code(mail, code, expires=REGIS_CODE_EXPIRES):
    if code in gen_regis_code(mail, expires=expires, if_check=True):
        return True
    return False

def gen_uid(seq=""):
    id = md5((str(time.time()) + seq).encode("utf-8")).hexdigest()
    if models.User.objects.filter(uid=id):
        id = gen_uid(seq=seq)
    return id

def check_login(request):
    return request.get_signed_cookie("uid", default=None, salt=COOKIE_SALT)

def create_user(mail, password, type, region):
    id = gen_uid(seq=mail)
    user_info = {"uid": id,
    "mail": mail,
    "password": password,
    "name": mail,
    "avatar": DEFAULT_AVATAR,
    "type": type,
    "region": region,
    "project": "",
    "regis_time": int(time.time()),
    "last_login_time": int(time.time()),
    "donate_history": "",
    "share_mail_history": ""}
    models.User.objects.create(**user_info)
    return user_info

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
        user_info = models.User.objects.filter(mail=mail).first()
        if not user_info:
            response_data["status"] = login_status["wrong_username"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif user_info.password != password:
            response_data["status"] = login_status["wrong_password"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            models.User.objects.filter(mail="ty_liang@foxmail.com").update(last_login_time=int(time.time()))
            response_data["status"] = login_status["success"]
            rep = HttpResponse(json.dumps(response_data), content_type="application/json")
            rep.set_signed_cookie("uid", user_info.uid, salt=COOKIE_SALT, max_age=COOKIE_EXPIRES, expires=COOKIE_EXPIRES, path=COOKIE_PATH)
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
            if models.User.objects.filter(mail=mail).first():
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
            password = data["passwod"]
            type = data["type"]
            region = data["region"]
            user_info = create_user(mail, password, type, region)
            response_data["status"] = regis_status["set_password_success"]
            return HttpResponse(json.dumps(response_data), content_type="application/json")

def logout(request):
    response_data = {"status": logout_status["not_logged_in"]}
    if not check_login(request):
        response_data["status"] = logout_status["not_logged_in"]
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data["status"] = logout_status["success"]
    rep = HttpResponse(json.dumps(response_data), content_type="application/json")
    rep.delete_cookie("uid")
    return rep