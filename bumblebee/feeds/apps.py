from django.apps import AppConfig


class FeedsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bumblebee.feeds"

    def ready(self):
        pass
