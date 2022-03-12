from django.test import TestCase
from DataBase import models
# Create your tests here.

userinfo = [{"uid": "1",
    "mail": "531273646@qq.com",
    "password": "123456",
    "name": "tyl",
    "avatar": "tyl.jpg",
    "type": 1,
    "region": "CHN",
    "currency_type": "GBP",
    "project": "",
    "regis_time": 1646958039,
    "last_login_time": 1646958139,
    "donate_history": "",
    "share_mail_history": ""},
    {"uid": "2",
    "mail": "ty_liang@foxmail.com",
    "password": "123456",
    "name": "tyl",
    "avatar": "tyl.jpg",
    "type": 2,
    "region": "CHN",
    "currency_type": "GBP",
    "project": "",
    "regis_time": 1646958039,
    "last_login_time": 1646958139,
    "donate_history": "",
    "share_mail_history": ""}]

projectinfo = [{"pid": str(i),
    "uid": "1",
    "title": str(i),
    "intro": str(i),
    "region": "CHN",
    "charity": "a",
    "charity_avatar": "tyl.jpg",
    "background_image": "tyl.jpg",
    "total_num": 100,
    "current_num": 0,
    "start_time": 1646958139,
    "end_time": 1647958139,
    "details": str(i),
    "price": 30,
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