from hashlib import md5
from DataBase.models import *
import time
from Common.common import *
from Login.functions import *

def gen_uid(seq=""):
    id = md5((str(time.time()) + seq).encode("utf-8")).hexdigest()
    if DUser.objects.filter(uid=id):
        id = gen_uid(seq=seq)
    return id

def create_user(create_info):
    param_list = ("mail", "password", "type", "region", "currency_type", "name", "avatar")
    if len(create_info) != len(param_list):
        return False
    for i in param_list:
        if i not in create_info:
            return False
    if create_info["type"] not in USER_TYPE.values():
        return False
    user_info = {"uid": "",
                 "project": "[]",
                 "regis_time": int(time.time()),
                 "last_login_time": int(time.time()),
                 "donate_history": "{}",
                 "share_mail_history": "[]"}
    user_info.update(create_info)
    user_info["region"] = region2rid(user_info["region"])
    if not user_info["region"]:
        return False
    user_info["currency_type"] = currency2cid(user_info["currency_type"])
    if not user_info["currency_type"]:
        return False
    if user_info["name"] == "":
        user_info["name"] = user_info["mail"]
    if user_info["avatar"] != "" and not os.path.isfile(os.path.join(IMG_DIR, os.path.basename(user_info["avatar"]))):
        user_info["avatar"] = ""
    user_info["uid"] = gen_uid(seq=user_info["mail"])
    return DUser.objects.create(**user_info)

def get_user(filter_dict):
    if len(filter_dict) != 1 or ("uid" not in filter_dict and "mail" not in filter_dict):
        return ""
    try:
        r = DUser.objects.get(**filter_dict)
        return r
    except:
        return ""

def add_project(user, pid):
    project = eval(user.project)
    project.append(pid)
    user.project = str(project)
    user.save(update_fields=["project"])
    return True

def get_user_decorator(force_login=True):
    def decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            request = args[0]
            user = check_login(request)
            if not user and force_login:
                response_data = {"status": ""}
                response_data["status"] = STATUS_CODE["user_not_logged_in"]
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            kwargs["user"] = user
            response = func(*args, **kwargs)
            return response
        return wrapped_function
    return decorator

def remove_project(user, pid):
    project = eval(user.project)
    if pid in project:
        project.remove(pid)
        user.project = str(project)
        user.save(update_fields=["project"])
    return True