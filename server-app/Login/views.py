#from django.shortcuts import render, redirect
from django.http import HttpResponse
from DataBase import models
from FoodForAll.settings import COOKIE_EXPIRES, COOKIE_PATH, COOKIE_SALT, REGIS_CODE_EXPIRES, DEFAULT_AVATAR
from Mail.views import Mail
import time
from hashlib import md5
import json

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
    response_data = {"status": "",
                     "username": "",
                     }
    if check_login(request):
        response_data["status"] = "is login"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == "GET":
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == "POST":
        data = json.loads(request.body)
        mail = data["username"]
        response_data["username"] = mail
        password = data["password"]
        user_info = models.User.objects.filter(mail=mail).first()
        if not user_info:
            response_data["status"] = "wrong username"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif user_info.passwd != password:
            response_data["status"] = "wrong password"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            models.User.objects.filter(mail="ty_liang@foxmail.com").update(last_login_time=int(time.time()))
            response_data["status"] = "success"
            return HttpResponse(json.dumps(response_data), content_type="application/json").\
                set_signed_cookie("uid", user_info.uid, salt=COOKIE_SALT, max_age=COOKIE_EXPIRES, expires=COOKIE_EXPIRES, path=COOKIE_PATH)

def regis(request):
    response_data = {"status": "",
                     "action": "",
                     }
    if check_login(request):
        response_data["status"] = "is login"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == "GET":
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    elif request.method == "POST":
        data = json.loads(request.body)
        mail = data["username"]
        action = data["action"]
        response_data["action"] = action
        if action == "send_code":
            if models.User.objects.filter(mail=mail).first():
                response_data["status"] = "mail has registed before"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            code = gen_regis_code(mail)
            try:
                Mail.regis_verify(mail, code)
                response_data["status"] = "mail sended"
            except:
                response_data["status"] = "mail wrong"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif action == "verify_code":
            code = data["code"]
            if check_regis_code(mail, code):
                response_data["status"] = "code verified"
            else:
                response_data["status"] = "code wrong"
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif action == "set_password":
            password = data["passwod"]
            type = data["type"]
            region = data["region"]
            user_info = create_user(mail, password, type, region)
            response_data["status"] = True
            return HttpResponse(json.dumps(response_data), content_type="application/json")

def logout(request):
    response_data = {"status": ""}
    if not check_login(request):
        response_data["status"] = "not login"
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    response_data["status"] = "success"
    return HttpResponse(json.dumps(response_data), content_type="application/json").delete_cookie("uid")