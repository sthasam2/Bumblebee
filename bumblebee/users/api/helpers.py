##############################
# data manipulation methods
#############################
def create_dict(**kwargs):
    """"""
    return dict(**kwargs)


def create_general_exception_response_dict(
    status: int, type: str, message: str, verbose=None
) -> dict:
    """
    creates a dictionary with error code, type, message
    """
    return {
        "status": status,
        "error": {
            "type": type,
            "message": message,
            "verbose": verbose,
        },
    }


def create_400_response_dict(status: int, type: str, message: str) -> dict:
    """
    creates a dictionary with error code, type, message
    """
    return {
        "status": status,
        "error": {
            "type": type,
            "message": message,
        },
    }


def create_200_response_dict(status: int, type: str, message: str) -> dict:
    """
    creates a dictionary with success code, type, message
    """
    return {
        "status": status,
        "success": {
            "type": type,
            "message": message,
        },
    }
