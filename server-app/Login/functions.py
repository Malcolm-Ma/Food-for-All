from User.functions import *
import random
import re
import base64 as b64

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
    s, t, u, a = decode_cookie(request, COOKIE_ENCODE_KEY)
    try:
        t = int(re.findall(r'[0-9]+', t)[0])
    except:
        return ""
    cookie_time = int(time.time()) - t
    url = get_request_url(request)
    agent = request.META['HTTP_USER_AGENT']
    if s and cookie_time >= 0 and cookie_time < COOKIE_EXPIRES and url == u[:len(url)] and agent == a[:len(agent)]:
        return get_user({"uid": s[:32]})
    return ""

def encode_cookie(request, uid, encode_key = COOKIE_ENCODE_KEY):
    random_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    s = uid
    t = str(int(time.time()))
    u = get_request_url(request)
    a = request.META['HTTP_USER_AGENT']
    length = max(len(s), len(t), len(u), len(a))
    merge = [""] * length * 4
    for i, j in enumerate((s, t, u, a)):
        j += "".join(random.choices(random_str, k=length - len(j)))
        merge[i::4] = j
    for i in re.findall(r'[1-9]', u):
        encode_key += int(i)
    c = ""
    for i in merge:
        c += chr(ord(i) ^ encode_key)
    return b64.b64encode(c.encode()).decode()

def decode_cookie(request, decode_key = COOKIE_ENCODE_KEY):
    url = get_request_url(request)
    cookie = request.get_signed_cookie(COOKIE_KEY, default=None, salt=COOKIE_SALT + url)
    try:
        cookie = b64.b64decode(cookie.encode()).decode()
    except:
        return "", "", "", ""
    if not cookie:
        return "", "", "", ""
    for i in re.findall(r'[1-9]', url):
        decode_key += int(i)
    c = ""
    for i in cookie:
        c += chr(ord(i) ^ decode_key)
    length = len(c) // 4
    s = c[0::4][:length]
    t = c[1::4][:length]
    u = c[2::4][:length]
    a = c[3::4][:length]
    return s, t, u, a