from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "bumblebee.users"

    def ready(self):
        import bumblebee.users.signals
