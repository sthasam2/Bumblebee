from django.apps import AppConfig


class BuzzesConfig(AppConfig):
    name = "bumblebee.buzzes"

    def ready(self):
        import bumblebee.buzzes.signals
