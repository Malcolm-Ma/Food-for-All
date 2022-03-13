from django.contrib import admin
from . models import User, Project

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'mail', 'password', 'name', 'avatar', 'type', 'region', 'currency_type', 'project', 'regis_time', 'last_login_time', 'donate_history', 'share_mail_history')
    list_filter = ['type', 'region', 'currency_type']
    search_fields = ['mail', 'name']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'pid', 'uid', 'title', 'intro', 'region', 'charity', 'charity_avatar', 'background_image', 'total_num', 'current_num', 'start_time', 'end_time', 'details', 'price', 'donate_history')
    list_filter = ['region']
    search_fields = ['title', 'intro', 'charity', 'details']

admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
