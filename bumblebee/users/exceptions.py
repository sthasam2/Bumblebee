"""
Custom Exceptions
"""


class Error(Exception):
    """
    Common base for all exceptions
    """

    pass


class PreExistenceError(Error):
    """
    Exception raised when a value already exists somewhere

    Parameters
    ---
    instance: given instance which caused error
    message: message for given error
    """

    def __init__(self, instance=None, message=None):
        self.instance = instance
        self.message = message

    def __str__(self):
        return f"""
        PreExistenceError:
        \n\tcause: {self.instance} 
        \n\tmessage: {self.message}
        \n\ttreeback: {self.with_traceback}
        """


class UnmatchedFieldsError(Error):
    """
    Exception raised when a value already exists somewhere

    Parameters
    ---
    instance: given instance which caused error
    message: message for given error
    """

    def __init__(self, instance=None, message=None):
        self.instance = instance
        self.message = message

    def __str__(self):
        return f"""
        UnmatchedFieldsError:
        \n\tcause: {self.instance}
        \n\tmessage: {self.message}
        \n\ttreeback: {self.with_traceback}
        """


class EmailNotVerifiedError(Error):
    """
    Exception raised when a user has not verified his email

    Parameters
    ---
    instance: given instance which caused error
    message: message for given error
    """

    def __init__(self, instance=None, message=None):
        self.instance = instance
        self.message = message

    def __str__(self):
        return f"""
        EmailNotVerifiedError:
        \n\tcause: {self.instance}
        \n\tmessage: {self.message}
        \n\ttreeback: {self.with_traceback}
        """
