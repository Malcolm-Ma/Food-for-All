from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class ApidocConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Apidoc'

    def ready(self):
        autodiscover_modules("apidoc.py")