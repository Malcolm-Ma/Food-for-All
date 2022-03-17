import json
from django.http import HttpResponse
from Project.functions import *
from User.functions import *

def init_database(request):
    models.User.objects.all().delete()
    models.Project.objects.all().delete()
    userinfo = [{"uid": gen_uid("a"),
                 "mail": "ty_liang@foxmail.com",
                 "password": "123456",
                 "name": "tyl",
                 "avatar": "",
                 "type": 1,
                 "region": "CN",
                 "currency_type": "CNY",
                 "project": "[]",
                 "regis_time": int(time.time() - 100),
                 "last_login_time": int(time.time() - 100),
                 "donate_history": "{}",
                 "share_mail_history": "[]"},
                {"uid": gen_uid("a"),
                 "mail": "531273646@qq.com",
                 "password": "123456",
                 "name": "tyl",
                 "avatar": "",
                 "type": 2,
                 "region": "CN",
                 "currency_type": "CNY",
                 "project": "[]",
                 "regis_time": int(time.time() - 100),
                 "last_login_time": int(time.time() - 100),
                 "donate_history": "{}",
                 "share_mail_history": "[]"}]
    for i in userinfo:
        models.User.objects.create(**i)
    projectinfo = [{"pid": gen_pid("as"),
                    "uid": get_user({"mail": "ty_liang@foxmail.com"}).uid,
                    "title": str(i),
                    "intro": str(i),
                    "region": "CN",
                    "charity": str(i),
                    "charity_avatar": "",
                    "background_image": "",
                    "total_num": 100,
                    "current_num": i,
                    "start_time": int(time.time() - 100 + i),
                    "end_time": int(time.time() + 365 * 24 * 60 * 60 + i),
                    "details": str(i),
                    "price": i,
                    "donate_history": ""} for i in range(1, 50)]
    for i in projectinfo:
        models.Project.objects.create(**i)
    models.User.objects.filter(mail="ty_liang@foxmail.com").update(
        project=str([i.pid for i in models.Project.objects.all()]))
    return HttpResponse(json.dumps({"status": 0}), content_type="application/json")