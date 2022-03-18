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
                "set_password_success": 6,
                "set_password_fail": 7}

regis_action = {"send_code": 0,
                "verify_code": 1,
                "set_password": 2}

logout_status = {"success": 0,
                 "not_logged_in": 1}

def check_login(request):
    s, t, u = decode_cookie(request)
    try:
        t = int(t)
    except:
        return ""
    cookie_time = int(time.time()) - t
    url = get_request_url(request)
    if s and cookie_time >= 0 and cookie_time < COOKIE_EXPIRES and u == url:
        return get_user({"uid": s})
    return ""

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