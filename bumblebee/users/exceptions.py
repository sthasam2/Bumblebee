"""
Custom Exceptions
"""


class Error(Exception):
    """
    Common base for all exceptions
    """

    pass


class CustomBaseError(Error):
    """
    Base for customized errors

    Parameters
    ---
    instance: given instance which caused error
    message: message for given error

    """

    name = None

    def __init__(self, instance=None, message=None):
        self.name = type(self).__name__
        self.instance = instance
        self.message = message

    def __str__(self):
        return f"""
        {self.name}:
        \n\tcause: {self.instance} 
        \n\tmessage: {self.message}
        \n\ttreeback: {self.with_traceback}
        """

    class Meta:
        abstract = True


class MissingFieldsError(CustomBaseError):
    """
    Exception raised when a value already exists somewhere
    """

    pass


class PreExistenceError(CustomBaseError):
    """
    Exception raised when a value already exists somewhere
    """

    pass


class NoneExistenceError(CustomBaseError):
    """
    Exception raised when a value already doesnt exists
    """

    pass


class UnmatchedFieldsError(CustomBaseError):
    """
    Exception raised when a value already exists somewhere
    """

    pass


class AlreadyEmailVerifiedError(CustomBaseError):
    """
    Exception raised when a user has not verified his email
    """

    pass


class EmailNotVerifiedError(CustomBaseError):
    """
    Exception raised when a user has not verified his email
    """

    pass


class ExpiredError(CustomBaseError):
    """
    Exception raised when a token is expired
    """

    pass
