from DataBase.models import *

# The code in this script defines a number of functional functions that the login system needs to use

# Function for generating encrypted cookies
def encode_cookie(request, uid, encode_key = COOKIE_ENCODE_KEY):
    random_str = string.ascii_letters
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

# Function for decrypting cookies
def decode_cookie(request, decode_key=COOKIE_ENCODE_KEY):
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

# Function for encrypting passwords (for password transmission)
def encode_password(password, encode_key=PASSWORD_ENCODE_KEY):
    encrypted_password = ""
    for i in password:
        encrypted_password += chr(ord(i) ^ encode_key)
    encrypted_password = b64.b64encode(encrypted_password.encode()).decode()
    return encrypted_password

# Function for decrypting passwords (for password transmission)
def decode_password(encrypted_password, decode_key=PASSWORD_ENCODE_KEY):
    encrypted_password = b64.b64decode(encrypted_password.encode()).decode()
    password = ""
    for i in encrypted_password:
        password += chr(ord(i) ^ decode_key)
    return password

# Function for detecting user login status
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

# Function for generating random CAPTCHA
def gen_verify_code(id_str, usefor_str, expires=VERIFY_CODE_EXPIRES):#, if_check=False):
    cache = caches[usefor_str]
    code = "".join(random.choices(string.digits + string.ascii_uppercase, k=6))
    cache.set(id_str, code, timeout=expires)
    return code

# Function to validate CAPTCHA
def check_verify_code(id_str, usefor_str, code, remove=False):#, expires=VERIFY_CODE_EXPIRES):
    cache = caches[usefor_str]
    real_code = cache.get(id_str)
    if real_code == code:
        if remove:
            cache.delete(id_str)
        return True
    return False