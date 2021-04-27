from ..utils import check_email_existence, check_username_existence


def check_email_username_valid(email: str, username: str) -> bool:
    """
    checks whether email and/or username already exists
    """
    email_exists = check_email_existence(email)
    username_exists = check_username_existence(username)
    if not email_exists and not username_exists:
        return False
    else:
        return True


# def create_validation_message()