from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class MycurdConfig(AppConfig):
    name = 'mycurd'

    def ready(self):
        """
        Override this method in subclasses to run code when Django starts.
        """
        autodiscover_modules('curd')
