from django.db import models

# Create your models here.
class User(models.Model):
    uid = models.CharField(max_length=64, unique=True)
    email = models.EmailField(unique=True)
    passwd = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    avatar = models.FilePathField(max_length=256)
    type = models.IntegerField()
    region = models.CharField(max_length=256)
    project = models.TextField()
    regis_time = models.TimeField()
    last_login_time = models.TimeField()