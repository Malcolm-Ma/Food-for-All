from django.contrib import admin
from . models import User, Project
from django.db import models
from django.forms import TextInput, Textarea

class UserAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 128})},
    }
    list_display = ('id', 'uid', 'mail', 'password', 'name', 'avatar', 'type', 'region', 'currency_type', 'short_project', 'regis_time', 'last_login_time', 'short_donate_history', 'share_mail_history')
    list_filter = ['type', 'region']
    search_fields = ['mail', 'name']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'pid', 'uid', 'title', 'intro', 'region', 'charity', 'charity_avatar', 'background_image', 'status', 'total_num', 'current_num', 'start_time', 'end_time', 'short_details', 'price', 'short_donate_history')
    list_filter = ['region', 'status']
    search_fields = ['title', 'intro', 'charity', 'details']

admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
