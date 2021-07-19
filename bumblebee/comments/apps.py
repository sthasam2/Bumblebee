from django.apps import AppConfig


class CommentsConfig(AppConfig):
    name = "bumblebee.comments"

    def ready(self):
        import bumblebee.comments.signals
