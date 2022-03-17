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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('region_list/', common_views.get_region_list),
    path('currency_list/', common_views.get_currency_list),
    path('region2currency/', common_views.get_region2currency),
    path('login/', login_views.login),
    path('regis/', login_views.regis),
    path('logout/', login_views.logout),
    path('get_user_info/', user_views.get_user_info),
    path('edit_user_info/', user_views.edit_user_info),
    path('get_project_info/', project_views.get_project_info),
    path('edit_project_info/', project_views.edit_project_info),
    path('get_projects_list/', project_views.get_projects_list),
    path('create_project/', project_views.create_project),
    path('delete_project/', project_views.delete_project),
    path('upload_img/', upload_views.upload_img),
    path('upload_doc/', upload_views.upload_doc),
    path('init_database/', database_views.init_database),
]