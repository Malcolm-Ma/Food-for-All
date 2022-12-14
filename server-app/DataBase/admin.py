from django.contrib import admin
from . models import DUser, DProject
from django.db import models
from django.forms import TextInput, Textarea

# The code in this script defines the database items that are displayed in the back-end administration interface

class UserAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 128})},
    }
    list_display = ('id', 'uid', 'mail', 'password', 'name', 'avatar', 'type', 'region', 'currency_type', 'short_project', 'regis_time', 'last_login_time', 'short_donate_history', 'share_mail_history')
    list_filter = ['type', 'region']
    search_fields = ['mail', 'name', "uid"]

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'pid', 'uid', 'title', 'intro', 'region', 'charity', 'charity_avatar', 'background_image', 'status', 'total_num', 'current_num', 'start_time', 'end_time', 'short_details', 'price', 'product_id', 'subscription_list', 'short_donate_history')
    list_filter = ['region', 'status']
    search_fields = ['title', 'intro', 'charity', 'details', "uid", "pid"]

admin.site.register(DUser, UserAdmin)
admin.site.register(DProject, ProjectAdmin)
