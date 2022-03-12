from django.shortcuts import render, redirect
from django.http import HttpResponse
from DataBase import models
from FoodForAll.settings import COOKIE_EXPIRES, COOKIE_PATH, COOKIE_SALT, MAIN_PATH, REGIS_CODE_EXPIRES
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

def gen_id(seq=""):
    id = md5((str(time.time()) + seq).encode("utf-8")).hexdigest()
    if models.User.objects.filter(uid=id):
        id = gen_id(seq=seq)
    return id

def login(request):
    if check_login(request):
        #return redirect(MAIN_PATH)
        return render(request, "login.html", {"status": "already login"})
    if request.method == "GET":
        return render(request, "login.html")
    mail = request.POST.get("username")
    password = request.POST.get("password")
    user_info = models.User.objects.filter(mail=mail).first()
    if not user_info:
        return render(request, "login.html", {"status": "invalid username"})
    elif user_info.passwd != password:
        return render(request, "login.html", {"status": "wrong password"})
    else:
        #rep = redirect(MAIN_PATH)
        rep = render(request, "login.html", {"status": "login success"})
        rep.set_signed_cookie("uid", user_info.uid, salt=COOKIE_SALT, max_age=COOKIE_EXPIRES, expires=COOKIE_EXPIRES, path=COOKIE_PATH)
        return rep

def regis(request):
    if request.method == "GET":
        return render(request, "regis.html")
    if request.POST.get("status") == "send_code":
        mail = request.POST.get("mail")
        code = gen_regis_code(mail)
        send_status = False
        try:
            Mail.regis_verify(mail, code)
            send_status = True
        except:
            pass
        rep = render(request, "regis.html", {"status":json.dumps(send_status)})
        return rep
    elif request.POST.get("status") == "verify_code":
        mail = request.POST.get("mail")
        code = request.POST.get("code")
        if check_regis_code(mail, code):
            rep = render(request, "regis.html", {"status":json.dumps(True)})
        else:
            rep = render(request, "regis.html", {"status":json.dumps(False)})
        return rep
    elif request.POST.get("status") == "set_passwd":
        # if check_passwd_valid():
        #     status, user_info = create_user()
        #     if status:
        #         pass
        #     else:
        #         pass
        #     pass
        # else:
            pass

def logout(request):
    if check_login(request):
        return render(request, "logout.html", {"status": "not login"})
    #rep = redirect(MAIN_PATH)
    rep = render(request, "logout.html", {"status": "logout success"})
    rep.delete_cookie("uid")
    return rep

def check_login(request):
    return request.get_signed_cookie("uid", default=None, salt=COOKIE_SALT)