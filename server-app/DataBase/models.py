from django.db import models

# Create your models here.
class User(models.Model):
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

class Project(models.Model):
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

class Param(models.Model):
    key = models.CharField(max_length=256)
    value = models.TextField()