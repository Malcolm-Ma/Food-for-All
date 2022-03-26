from DataBase.models import *

regis_action = {"send_code": 0,
                "verify_code": 1,
                "set_password": 2}

reset_password_action = {"send_code": 0,
                         "verify_code": 1,
                         "set_password": 2}

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
        return DUser.get_user({"uid": s[:32]})
    return ""