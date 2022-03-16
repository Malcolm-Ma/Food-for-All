from hashlib import md5
from DataBase import models
import time
from Common.common import *

edit_user_info_status = {"success": 0,
                         "not_logged_in": 1,
                         "fail": 2}

user_type = {"admin": 0,
             "charity": 1,
             "guest": 2}

user_info_dict = {"mail": "",
                  "name": "",
                  "avatar": "",
                  "type": "",
                  "region": "",
                  "currency_type": "",
                  "project": "",
                  "regis_time": 0,
                  "last_login_time": 0,
                  "donate_history": "",
                  "share_mail_history": ""}

def gen_uid(seq=""):
    id = md5((str(time.time()) + seq).encode("utf-8")).hexdigest()
    if models.User.objects.filter(uid=id):
        id = gen_uid(seq=seq)
    return id

def create_user(create_info):
    param_list = ("mail", "password", "type", "region", "currency_type", "name", "avatar")
    if len(create_info) != len(param_list):
        return False
    for i in param_list:
        if i not in create_info:
            return False
    if create_info["type"] not in user_type.values():
        return False
    user_info = {"uid": "",
                 "project": "{}",
                 "regis_time": int(time.time()),
                 "last_login_time": int(time.time()),
                 "donate_history": "{}",
                 "share_mail_history": ","}
    user_info.update(create_info)
    user_info["region"] = region2rid(user_info["region"])
    if not user_info["region"]:
        return False
    user_info["currency_type"] = currency2cid(user_info["currency_type"])
    if not user_info["currency_type"]:
        return False
    if user_info["name"] == "":
        user_info["name"] = user_info["mail"]
    if user_info["avatar"] != "" and not os.path.isfile(os.path.join(IMG_PATH, os.path.basename(user_info["avatar"]))):
        user_info["avatar"] = ""
    user_info["uid"] = gen_uid(seq=user_info["mail"])
    return models.User.objects.create(**user_info)

def filter_user_info(filter_dict):
    return models.User.objects.filter(**filter_dict)

def update_user_info(user_query, update_dict):
    if "region" in update_dict:
        if update_dict["region"] in REGION2RID:
            update_dict["region"] = REGION2RID[update_dict["region"]]
        elif update_dict["region"] not in RID2REGION:
            return False
    if "currency_type" in update_dict:
        if update_dict["currency_type"] in CURRENCY2CID:
            update_dict["currency_type"] = CURRENCY2CID[update_dict["currency_type"]]
        elif update_dict["currency_type"] not in CID2CURRENCY:
            return False
    return user_query.update(**update_dict)