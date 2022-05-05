"""FoodForAll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from Login import views as login_views
from User import views as user_views
from Project import views as project_views
from Common import views as common_views
from Upload import views as upload_views
from DataBase import views as database_views
from Share import views as share_views
from Payment import views as payment_views
from Statistics import views as statistics_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('region_list/', common_views.get_region_list),
    path('currency_list/', common_views.get_currency_list),
    path('region2currency/', common_views.get_region2currency),
    path('get_ip_info/', common_views.get_ip_info),
    path('login/', login_views.login),
    path('regis/', login_views.regis),
    path('logout/', login_views.logout),
    path('reset_password/', login_views.reset_password),
    path('get_user/', user_views.get_user),
    path('edit_user/', user_views.edit_user),
    path('get_project/', project_views.get_project),
    path('edit_project/', project_views.edit_project),
    path('get_projects_list/', project_views.get_projects_list),
    path('get_prepare_projects_list/', project_views.get_prepare_projects_list),
    path('create_project/', project_views.create_project),
    path('delete_project/', project_views.delete_project),
    path('start_project/', project_views.start_project),
    path('suspend_project/', project_views.suspend_project),
    path('stop_project/', project_views.stop_project),
    path('upload_img/', upload_views.upload_img),
    path('upload_doc/', upload_views.upload_doc),
    path('share_by_email/', share_views.share_by_email),
    path('pay/', payment_views.pay),
    path('capture_payment/', payment_views.capture_payment),
    path('get_stat/', statistics_views.get_stat),
    path('get_report/', statistics_views.get_report),
    path('init_database/', database_views.init_database),
]