import time
from hashlib import md5
from Common.common import *
from User.functions import *

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

def check_login(request):
    s, t, u = decode_cookie(request)
    try:
        t = int(t)
    except:
        return ""
    cookie_time = int(time.time()) - t
    url = get_request_url(request)
    if s and cookie_time > 0 and cookie_time < COOKIE_EXPIRES and u == url:
        return filter_user_info({"uid": s}).first()
    return ""

def get_request_url(request):
    url = request.META.get('HTTP_X_FORWARDED_FOR')
    if not url:
        url = request.META.get('REMOTE_ADDR')
    return url

def encode_cookie(request, uid):
    t = str(int(time.time())).ljust(len(uid), "#")
    s = uid.ljust(len(t), "#")
    u = get_request_url(request).ljust(len(t), "#")
    return s + t + u

def decode_cookie(request):
    cookie = request.get_signed_cookie("apex", default=None, salt=COOKIE_SALT)
    if not cookie:
        return "", "", ""
    s = cookie[:32]
    t = cookie[int(len(cookie)/3):int(len(cookie)*2/3)].replace("#", "")
    u = cookie[int(len(cookie)*2/3):].replace("#", "")
    return s, t, u