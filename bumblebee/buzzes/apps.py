from django.apps import AppConfig


class BuzzConfig(AppConfig):
    name = "bumblebee.buzzes"

    def ready(self):
        import bumblebee.buzzes.signals