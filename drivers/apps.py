
from django.apps import AppConfig


class DriversConfig(AppConfig):
    name = 'drivers'

    def ready(self):
        import drivers.signals
