from .functions import *

COOKIE_KEY = "apex"
COOKIE_EXPIRES = 7 * 24 * 60 * 60
COOKIE_PATH = "/"
COOKIE_SALT = "apex"
COOKIE_ENCODE_KEY = 80

VERIFY_CODE_EXPIRES = 30 * 60
VERIFY_CODE_KEY_REGIS = "regis"
VERIFY_CODE_KEY_RESET_PASSWORD = "reset_password"

REGION2RID, RID2REGION = create_region_list()
CURRENCY2CID, CID2CURRENCY = create_currency_list()
RID2CID = create_region_currency_list()
EXCHANGE_RATE = create_exchange_rate()
REGION2CURRENCY = dict([[RID2REGION[i], CID2CURRENCY[j]] for i,j in RID2CID.items()])

logger_standard = logging.getLogger('standard')

USER_TYPE = {"admin": 0,
             "charity": 1,
             "guest": 2}

def region2rid(region):
    if region in REGION2RID:
        return REGION2RID[region]
    elif region in RID2REGION:
        return region
    else:
        return ""

def rid2region(rid):
    if rid2region in RID2REGION:
        return RID2REGION[rid2region]
    elif rid2region in REGION2RID:
        return rid2region
    else:
        return ""

def currency2cid(currency):
    if currency in CURRENCY2CID:
        return CURRENCY2CID[currency]
    elif currency in CID2CURRENCY:
        return currency
    else:
        return ""

def cid2currency(cid):
    if cid in CID2CURRENCY:
        return CID2CURRENCY[cid]
    elif cid in CURRENCY2CID:
        return cid
    else:
        return ""

def gen_verify_code(id_str, usefor_str, expires=VERIFY_CODE_EXPIRES, if_check=False):
    dynamic_num = int(time.time()) // expires
    code1 = md5((str(dynamic_num) + id_str + usefor_str).encode("utf-8")).hexdigest()[:6]
    if not if_check:
        return code1
    code2 = md5((str(dynamic_num - 1) + id_str + usefor_str).encode("utf-8")).hexdigest()[:6]
    return code1, code2

def check_verify_code(id_str, usefor_str, code, expires=VERIFY_CODE_EXPIRES):
    if code in gen_verify_code(id_str, usefor_str, expires=expires, if_check=True):
        return True
    return False

def get_request_url(request):
    url = request.META.get('HTTP_X_FORWARDED_FOR')
    if not url:
        url = request.META.get('REMOTE_ADDR')
    return url

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
        try:
            user = models.User.objects.get(**{"uid": s[:32]})
            return user
        except:
            return ""
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

def api_logger(logger):
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            response = func(*args, **kwargs)
            logger.info("[{uid}] - [Request] [{url}] [{method}] [{path_info}] [{request_data}] - [Response] [{status_code}] [{response_data}]".format(url=get_request_url(request), method=request.method, path_info=request.path_info, request_data=request.body.decode(), status_code=str(response.status_code), response_data=response.content.decode(), uid="guest" if not check_login(request) else check_login(request).uid))
            return response
        return wrapped_function
    return logging_decorator