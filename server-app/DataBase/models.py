from django.db import models
from Common.common import *
from django.db.models import F, Q
import math

USER_TYPE = {"admin": 0,
             "charity": 1,
             "guest": 2}

PROJECT_STATUS = {"prepare": 0,
                  "ongoing": 1,
                  "finish": 2}

class DUser(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    mail = models.EmailField(unique=True)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    avatar = models.FilePathField(max_length=256)
    type = models.IntegerField()
    region = models.CharField(max_length=256)
    currency_type = models.CharField(max_length=256)
    project = models.TextField()
    regis_time = models.IntegerField()
    last_login_time = models.IntegerField()
    donate_history = models.TextField()
    share_mail_history = models.CharField(max_length=512)

    def to_dict(self, fields=tuple()):
        user_dict = {}
        allow_fields = ("uid", "mail", "name", "avatar", "type", "region", "currency_type", "project", "regis_time", "last_login_time", "donate_history", "share_mail_history")#, "password"
        fields = allow_fields if not fields else [i for i in fields if i in allow_fields]
        for i in fields:
            user_dict[i] = self.__getattribute__(i)
        for i in ("project", "donate_history", "share_mail_history"):
            if i in fields:
                user_dict[i] = eval(user_dict[i])
        return user_dict

    def update_from_fict(self, update_dict):
        allow_fields = ("mail", "password", "name", "avatar", "type", "region", "currency_type", "last_login_time", "share_mail_history")
        update_fields = [i for i in update_dict if i in allow_fields]
        if "type" in update_fields and update_dict["type"] not in USER_TYPE.values():
            return False
        if "region" in update_fields:
            update_dict["region"] = region2rid(update_dict["region"])
            if not update_dict["region"]:
                return False
        if "currency_type" in update_fields:
            update_dict["currency_type"] = currency2cid(update_dict["currency_type"])
            if not update_dict["currency_type"]:
                return False
        if "share_mail_history" in update_fields:
            update_dict["share_mail_history"] = str(update_dict["share_mail_history"])
        try:
            for key in update_fields:
                self.__setattr__(key, update_dict[key])
            self.save(update_fields=update_fields)
            return True
        except:
            return False

    @staticmethod
    def create(create_dict):
        must_fields = ["mail", "password", "type", "region", "currency_type", "name", "avatar"]
        if not set(must_fields) == set(create_dict.keys()):
            return False
        if create_dict["type"] not in USER_TYPE.values():
            return False
        default_dict = {"uid": "",
                        "project": "[]",
                        "regis_time": int(time.time()),
                        "last_login_time": int(time.time()),
                        "donate_history": "{}",
                        "share_mail_history": "[]"}
        create_dict.update(default_dict)
        create_dict["region"] = region2rid(create_dict["region"])
        if not create_dict["region"]:
            return False
        create_dict["currency_type"] = currency2cid(create_dict["currency_type"])
        if not create_dict["currency_type"]:
            return False
        if create_dict["name"] == "":
            create_dict["name"] = create_dict["mail"]
        if create_dict["avatar"] != "" and not check_url_file_exist(create_dict["avatar"], "img"):
            create_dict["avatar"] = ""
        create_dict["uid"] = DUser.gen_uid(seq=create_dict["mail"])
        try:
            DUser.objects.create(**create_dict)
            return True
        except:
            return False

    def create_project(self):
        if self.type != USER_TYPE["charity"]:
            return STATUS_CODE["user_not_charity"], -1
        create_dict = {}
        create_dict["uid"] = self.uid
        create_dict["title"] = ""
        create_dict["intro"] = ""
        create_dict["region"] = self.region
        create_dict["charity"] = self.name
        create_dict["charity_avatar"] = self.avatar
        create_dict["background_image"] = ""
        create_dict["status"] = PROJECT_STATUS["prepare"]
        create_dict["total_num"] = 0
        create_dict["current_num"] = 0
        create_dict["start_time"] = 0
        create_dict["end_time"] = 0
        create_dict["details"] = ""
        create_dict["price"] = 0
        create_dict["donate_history"] = "{}"
        create_dict["pid"] = DProject.gen_pid(self.mail)
        try:
            DProject.objects.create(**create_dict)
            self.add_project_to_list(create_dict["pid"])
            return STATUS_CODE["success"], create_dict["pid"]
        except:
            return STATUS_CODE["create_project_fail"], -1

    def delete_project(self, project):
        if project.uid != self.uid:
            return STATUS_CODE["user_not_project_owner"]
        if project.status != PROJECT_STATUS["prepare"]:
            return STATUS_CODE["project_non_deletable"]
        remove_url_file(project.background_image, "img")
        self.delete_project_from_list(project.pid)
        project.delete()
        return STATUS_CODE["success"]

    def add_project_to_list(self, pid):
        project = eval(self.project)
        project.append(pid)
        self.project = str(project)
        self.save(update_fields=["project"])
        return STATUS_CODE["success"]

    def delete_project_from_list(user, pid):
        project = eval(user.project)
        if pid in project:
            project.remove(pid)
            user.project = str(project)
            user.save(update_fields=["project"])
        return STATUS_CODE["success"]

    @staticmethod
    def gen_uid(seq=""):
        id = md5((str(time.time()) + seq).encode("utf-8")).hexdigest()
        if DUser.objects.filter(uid=id):
            id = DUser.gen_uid(seq=seq)
        return id

    @staticmethod
    def get_user(filter_dict):
        if len(filter_dict) != 1 or ("uid" not in filter_dict and "mail" not in filter_dict):
            return ""
        try:
            r = DUser.objects.get(**filter_dict)
            return r
        except:
            return ""

    def short_donate_history(self):
        max_len = 256
        if len(str(self.donate_history)) > max_len:
            return '{}...'.format(str(self.donate_history)[:max_len])
        else:
            return str(self.donate_history)

    def short_project(self):
        max_len = 256
        if len(str(self.project)) > max_len:
            return '{}...'.format(str(self.project)[:max_len])
        else:
            return str(self.project)

class DProject(models.Model):
    pid = models.CharField(max_length=64, unique=True)
    uid = models.CharField(max_length=64)
    title = models.CharField(max_length=256)
    intro = models.CharField(max_length=256)
    region = models.CharField(max_length=256)
    charity = models.CharField(max_length=256)
    charity_avatar = models.FilePathField(max_length=256)
    background_image = models.FilePathField(max_length=256)
    status = models.IntegerField()
    total_num = models.IntegerField()
    current_num = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    details = models.TextField()
    price = models.FloatField()
    donate_history = models.TextField()

    def to_dict(self, fields=tuple(), currency_type=""):
        self.auto_update_status()
        project_dict = {}
        allow_fields = ("pid", "uid", "title", "intro", "region", "charity", "charity_avatar", "background_image", "status", "total_num", "current_num", "start_time", "end_time", "details", "price", "donate_history")
        fields = allow_fields if not fields else [i for i in fields if i in allow_fields]
        for i in fields:
            project_dict[i] = self.__getattribute__(i)
        for i in ("donate_history", ):
            if i in fields:
                project_dict[i] = eval(project_dict[i])
        if currency_type and "price" in fields:
            cid = currency2cid(currency_type)
            if cid:
                project_dict["price"] = project_dict["price"] * EXCHANGE_RATE[cid]
            else:
                return {}
        return project_dict

    def auto_update_status(self):
        if self.status == PROJECT_STATUS["ongoing"] and (self.end_time <= int(time.time()) or self.current_num >= self.total_num):
            self.status = PROJECT_STATUS["finish"]
            self.save(update_fields=["status"])
            #if error, log

    def update_from_fict(self, update_dict):
        allow_fields = ("title", "intro", "background_image", "status", "total_num", "current_num", "start_time", "end_time", "details", "price", "donate_history")
        update_fields = [i for i in update_dict if i in allow_fields]
        if "status" in update_fields and update_dict["status"] not in PROJECT_STATUS.values():
            return False
        if "end_time" in update_fields and update_dict["end_time"] < int(time.time()):
            return False
        if "price" in update_fields and update_dict["price"] <= 0:
            return False
        if "donate_history" in update_fields:
            update_dict["donate_history"] = str(update_dict["donate_history"])
        try:
            for key in update_fields:
                self.__setattr__(key, update_dict[key])
            self.save(update_fields=update_fields)
            return True
        except:
            return False

    @staticmethod
    def gen_pid(seq=""):
        id = md5((str(time.time()) + seq).encode("utf-8")).hexdigest()
        if DProject.objects.filter(pid=id):
            id = DProject.gen_pid(seq=seq)
        return id

    @staticmethod
    def get_project(filter_dict):
        if len(filter_dict) != 1 or "pid" not in filter_dict:
            return ""
        try:
            r = DProject.objects.get(**filter_dict)
            return r
        except:
            return ""

    def short_details(self):
        max_len = 256
        if len(str(self.details)) > max_len:
            return '{}...'.format(str(self.details)[:max_len])
        else:
            return str(self.details)

    def short_donate_history(self):
        max_len = 256
        if len(str(self.donate_history)) > max_len:
            return '{}...'.format(str(self.donate_history)[:max_len])
        else:
            return str(self.donate_history)

class DProjectQuery(object):

    order_list = ["title", "-title", "charity", "-charity", "price", "-price",
                  "start_time", "-start_time", "end_time", "-end_time", "progress", "-progress"]

    def __init__(self):
        self.model = DProject
        self.query = ""

    def to_dict(self, fields=tuple(), currency_type=""):
        projects_dict = {}
        allow_fields = ("pid", "uid", "title", "intro", "region", "charity", "charity_avatar", "background_image", "status", "total_num", "current_num", "start_time", "end_time", "details", "price", "donate_history")
        fields = allow_fields if not fields else [i for i in fields if i in allow_fields]
        if currency_type and "price" in fields and not currency2cid(currency_type):
            return projects_dict
        for i in range(len(self.query)):
            projects_dict[str(i)] = self.query[i].to_dict(fields=fields, currency_type=currency_type)
        return projects_dict

    def get_all(self, uid=""):
        if uid:
            self.query = self.model.objects.filter(uid=uid)
        else:
            self.query = self.model.objects.all()
        return self.query

    def get_ready(self, uid="", valid_only=1):
        exclude_conditions = {}
        filter_conditions = {}
        if valid_only:
            filter_conditions.update({"status": PROJECT_STATUS["ongoing"], "current_num__lt": F("total_num"), "end_time__gt": int(time.time())})
        else:
            exclude_conditions.update({"status": PROJECT_STATUS["prepare"]})
        if uid:
            filter_conditions.update({"uid": uid})
        self.query = self.model.objects.filter(**filter_conditions).exclude(**exclude_conditions)
        return self.query

    def get_prepare(self, uid):
        self.query = self.model.objects.filter(**{"uid": uid, "status": PROJECT_STATUS["prepare"]})
        return self.query

    def order_by(self, order):
        if order not in self.order_list:
            return ""
        if not self.query:
            return self.query
        if order == "progress":
            order = F('current_num') / F('total_num')
        elif order == "-progress":
            order = -F('current_num') / F('total_num')
        self.query = self.query.order_by(order)
        return self.query

    def search(self, key_word):
        if key_word == "" or not self.query:
            return self.query
        q = Q()
        for w in key_word.split():
            q = q | Q(title__icontains=w) | Q(intro__icontains=w) | Q(charity__icontains=w)  # | Q(details__icontains = w)
        self.query = self.query.filter(q)
        return self.query

    def filter(self, current_batch, batch_size, order, key_word, currency_type):
        self.query.search(key_word)
        self.query.order_by(order)
        total_num = len(self.query)
        batch_num = math.ceil(total_num / batch_size)
        self.query = self.query[(current_batch - 1) * batch_size: min(current_batch * batch_size, total_num)]
        projects_dict = self.to_dict(fields=["pid", "uid", "title", "intro", "region",
                                             "charity", "charity_avatar", "background_image", "price",
                                             "current_num", "total_num", "start_time", "end_time", "status"],
                                             currency_type=currency_type)
        return projects_dict, batch_num

class Param(models.Model):
    key = models.CharField(max_length=256)
    value = models.TextField()