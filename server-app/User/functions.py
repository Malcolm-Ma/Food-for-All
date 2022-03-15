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

def create_user(mail, password, type, region, currency_type, name="", avatar=DEFAULT_AVATAR):
    id = gen_uid(seq=mail)
    if region not in REGION2RID:
        region = "GB"
    else:
        region = REGION2RID[region]
    if currency_type not in CURRENCY2CID:
        currency_type = "GBP"
    else:
        currency_type = CURRENCY2CID[currency_type]
    if name == "":
        name = mail
    user_info = {"uid": id,
    "mail": mail,
    "password": password,
    "name": name,
    "avatar": avatar,
    "type": type,
    "region": region,
    "currency_type": currency_type,
    "project": "{}",
    "regis_time": int(time.time()),
    "last_login_time": int(time.time()),
    "donate_history": "{}",
    "share_mail_history": ","}
    models.User.objects.create(**user_info)
    return user_info

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