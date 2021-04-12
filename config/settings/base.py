import os

from django.core.exceptions import ImproperlyConfigured


def get_environ_variable(var_name: str) -> str:
    """
    Get the environment variable from your os or return an exception
    """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = f"{var_name} not found!\nSet the '{var_name}' environment variable"
        raise ImproperlyConfigured(error_msg)