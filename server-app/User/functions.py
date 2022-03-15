from hashlib import md5
from DataBase import models
import time
from Common.common import *

user_type = {"admin": 0,
             "charity": 1,
             "guest": 2}

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
    return user_query.update(**update_dict)