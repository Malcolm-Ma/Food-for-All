from .functions import *
from .utils import *

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

STATUS_CODE = {"success": 0,
               "user_not_logged_in": 100001,
               "edit_user_info_fail": 100002,
               "user_not_charity": 100003,
               "user_already_logged_in": 100004,
               "wrong_username": 100005,
               "wrong_password": 100006,
               "mail_already_registered": 100007,
               "set_password_fail": 100008,
               "mail_not_registered": 100009,
               "user_not_match": 100010,
               "create_project_fail": 200001,
               "project_not_exists": 200002,
               "user_not_project_owner": 200003,
               "project_non_deletable": 200004,
               "edit_project_fail": 200005,
               "project_non_editable": 200006,
               "project_information_incomplete": 200007,
               "start_project_fail": 200008,
               "project_non_startable": 200009,
               "stop_project_fail": 200010,
               "project_non_stopable": 200011,
               "project_end_time_invalid": 200012,
               "wrong_currency_type": 300001,
               "mail_send_fail": 300002,
               "code_verify_fail": 300003,
               "wrong_action": 300004,
               "request_parameters_wrong": 400001,
               }

def region2rid(region):
    if region in REGION2RID:
        return REGION2RID[region]
    elif region in RID2REGION:
        return region
    else:
        return ""

def rid2region(rid):
    if rid in RID2REGION:
        return RID2REGION[rid]
    elif rid in REGION2RID:
        return rid
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

def check_request_method_decorator(method=("POST",)):
    if type(method) == str:
        method = [method]
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            if request.method not in method:
                return HttpResponseNotAllowed(method)
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator

def check_request_parameters_decorator(params=()):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            if params:
                request = args[0]
                data = json.loads(request.body)
                for i in params:
                    if i not in data:
                        response_data = {"status": STATUS_CODE["request_parameters_wrong"]}
                        return HttpResponseBadRequest(json.dumps(response_data), content_type="application/json")
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator