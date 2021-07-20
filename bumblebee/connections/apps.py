from django.apps import AppConfig


class ConnectionsConfig(AppConfig):
    name = "bumblebee.connections"

    def ready(self):
        import bumblebee.connections.signals
