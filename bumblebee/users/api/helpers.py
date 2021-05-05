##############################
# data manipulation methods
#############################
from bumblebee.users.exceptions import ExtraFieldsError, MissingFieldsError


def create_dict(**kwargs):
    """ """
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


def create_400_response_dict(status: int, message: str, detail: str) -> dict:
    """
    creates a dictionary with error code, message, detail
    """
    return {
        "status": status,
        "error": {
            "message": message,
            "detail": detail,
        },
    }


def create_200_response_dict(status: int, message: str, detail: str) -> dict:
    """
    creates a dictionary with success code, message, message
    """
    return {
        "status": status,
        "success": {
            "message": message,
            "detail": detail,
        },
    }


class RequestFieldsChecker:
    """ """

    def check_at_least_one_field_or_raise(
        self, req_body: dict, field_options: list
    ) -> None:
        """ """

        included = list()
        for key, value in req_body.items():
            if key in field_options:
                included.append(key)

        if len(included) == 0:
            raise MissingFieldsError(
                message=create_400_response_dict(
                    400,
                    "Missing Fields",
                    f"No fields from required were provided",
                ),
            )
        else:
            return None

    def check_extra_fields_or_raise(
        self, req_body: dict, field_options: list, required_fields: list = None
    ) -> None:
        """ """

        extra = list()
        for key, value in req_body.items():
            if key not in field_options and key not in required_fields:
                extra.append(key)

        if len(extra) != 0:
            raise ExtraFieldsError(
                message=create_400_response_dict(
                    400,
                    "Extra Fields",
                    f"Extra fields were provided: \n {extra}",
                ),
            )
        else:
            return None

    def check_required_field_or_raise(self, req_body, required_fields: list) -> None:
        """ """

        included = list()
        for key, value in req_body.items():
            if key in required_fields:
                included.append(key)

        missing = set(required_fields) - set(included)

        if len(missing) != 0:
            raise MissingFieldsError(
                missing,
                create_400_response_dict(
                    400,
                    "Missing Fields",
                    f"The following required fields are missing:\n {missing}",
                ),
            )
        else:
            return None
