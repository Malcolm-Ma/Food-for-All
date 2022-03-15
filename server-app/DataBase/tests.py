import time

from django.test import TestCase
from DataBase import models
from Project.functions import *
from User.functions import *
from Common.common import *

userinfo = [{"uid": "1",
    "mail": "ty_liang@foxmail.com",
    "password": "123456",
    "name": "tyl",
    "avatar": DEFAULT_AVATAR,
    "type": 1,
    "region": "CN",
    "currency_type": "CNY",
    "project": "",
    "regis_time": int(time.time() - 100),
    "last_login_time": int(time.time() - 100),
    "donate_history": "",
    "share_mail_history": ""},
    {"uid": "2",
    "mail": "531273646@qq.com",
    "password": "123456",
    "name": "tyl",
    "avatar": DEFAULT_AVATAR,
    "type": 2,
    "region": "CN",
    "currency_type": "CNY",
    "project": "",
    "regis_time": int(time.time() - 100),
    "last_login_time": int(time.time() - 100),
    "donate_history": "",
    "share_mail_history": ""}]

projectinfo = [{"pid": gen_pid("as"),
    "uid": filter_user_info({"mail": "ty_liang@foxmail.com"})[0].uid,
    "title": str(i),
    "intro": str(i),
    "region": "CN",
    "charity": "a",
    "charity_avatar": DEFAULT_AVATAR,
    "background_image": "",
    "total_num": 100,
    "current_num": 0,
    "start_time": int(time.time() - 100),
    "end_time": int(time.time() + 365*24*60*60),
    "details": str(i),
    "price": i,
    "donate_history": ""} for i in range(1, 50)]

class Test(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user(self):
        for i in userinfo:
            models.User.objects.create(**i)
        q = models.User.objects.all()
        print("User table num after create 2: {num}\n".format(num=str(len(q))))
        for i in q:
            for k, v in i.__dict__.items():
                print("{k}: {v}".format(k=k, v=v))
            print()

    def test_project(self):
        for i in projectinfo:
            models.Project.objects.create(**i)
        q = models.User.objects.all()
        print("User table num after create 2: {num}\n".format(num=str(len(q))))
        for i in q:
            for k, v in i.__dict__.items():
                print("{k}: {v}".format(k=k, v=v))
            print()

    def test_project(self):
        pass

def init_database():
    models.User.objects.all().delete()
    models.Project.objects.all().delete()
    userinfo = [{"uid": "1",
                 "mail": "ty_liang@foxmail.com",
                 "password": "123456",
                 "name": "tyl",
                 "avatar": DEFAULT_AVATAR,
                 "type": 1,
                 "region": "CN",
                 "currency_type": "CNY",
                 "project": "",
                 "regis_time": int(time.time() - 100),
                 "last_login_time": int(time.time() - 100),
                 "donate_history": "",
                 "share_mail_history": ""},
                {"uid": "2",
                 "mail": "531273646@qq.com",
                 "password": "123456",
                 "name": "tyl",
                 "avatar": DEFAULT_AVATAR,
                 "type": 2,
                 "region": "CN",
                 "currency_type": "CNY",
                 "project": "",
                 "regis_time": int(time.time() - 100),
                 "last_login_time": int(time.time() - 100),
                 "donate_history": "",
                 "share_mail_history": ""}]
    for i in userinfo:
        models.User.objects.create(**i)
    projectinfo = [{"pid": gen_pid("as"),
                    "uid": filter_user_info({"mail": "ty_liang@foxmail.com"})[0].uid,
                    "title": str(i),
                    "intro": str(i),
                    "region": "CN",
                    "charity": "a",
                    "charity_avatar": DEFAULT_AVATAR,
                    "background_image": "",
                    "total_num": 100,
                    "current_num": 0,
                    "start_time": int(time.time() - 100),
                    "end_time": int(time.time() + 365 * 24 * 60 * 60),
                    "details": str(i),
                    "price": i,
                    "donate_history": ""} for i in range(1, 50)]
    for i in projectinfo:
        models.Project.objects.create(**i)
    models.User.objects.filter(mail="ty_liang@foxmail.com").update(
        project=str([i.pid for i in models.Project.objects.all()]))