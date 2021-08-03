from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = "bumblebee.profiles"

    def ready(self):
        import bumblebee.profiles.signals
