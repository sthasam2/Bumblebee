from django.contrib.auth.base_user import BaseUserManager

from config.definitions import DEBUG

# from .exceptions import PreExistenceError, UnmatchedFieldsError
# from .utils import check_email_existence, check_username_existence


class CustomUserManager(BaseUserManager):
    """
    Custom function for creating users i.e. user manager using djangos BaseUserManager
    """

    def _create_user(
        self,
        username: str,
        email: str,
        password: str,
        is_email_verified: bool,
        **extra_fields,
    ):
        """
        Creates and saves a User with given fields
        """
        if not username:
            raise ValueError("username is mandatory")
        if not email:
            raise ValueError("Email is mandatory")
        if not password:
            raise ValueError("Password is mandatory")

        email = self.normalize_email(email)
        new_user = self.model(email=email, username=username)
        new_user.set_password(password)
        new_user.email_verified = is_email_verified

        new_user.admin = extra_fields["is_superuser"]
        new_user.staff = extra_fields["is_staff"]
        new_user.active = extra_fields["is_active"]

        new_user.save(using=self._db)
        if DEBUG:
            print("SUCCESS: New User Created!")

        return new_user

    def _check_required_fields(self, **req_fields):
        """
        Checks required fields
        """

        if not req_fields["username"]:
            raise ValueError("username is mandatory")
        if not req_fields["email"]:
            raise ValueError("Email is mandatory")
        if not req_fields["password"]:
            raise ValueError("Password is mandatory")

    def _check_extra_fields(self, **extra_fields):
        """
        Checks the extra fields
        """
        keys_valuestype = {
            "is_active": bool(),
            "is_staff": bool(),
            "is_superuser": bool(),
        }
        # check missing keys
        diff = set(keys_valuestype) - set(extra_fields)
        if len(diff) != 0:
            raise ValueError(
                f"Missing Fields: The following fields are missing: {diff} "
            )

        # check unnecessary fields
        unnecessary = set(extra_fields) - set(keys_valuestype)
        if len(unnecessary) != 0:
            raise KeyError(
                f"Unnecessary Fields: The following fields are unnecessary: \t{unnecessary}"
            )

        # check type of entered values
        for key, value in extra_fields.items():
            if not isinstance(value, type(keys_valuestype[key])):
                raise TypeError(
                    f"{key} must have value of type '{type(keys_valuestype[key]).__name__}'"
                )

        return True

    def create_user(self, username, email, password, **extra_fields):
        """
        Creates a regular user
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        if self._check_extra_fields(**extra_fields):
            return self._create_user(username, email, password, False, **extra_fields)

    def create_staffuser(self, username, email, password, **extra_fields):
        """
        Creates a is_staff user
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)

        if self._check_extra_fields(**extra_fields):
            return self._create_user(username, email, password, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates a super user
        """
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if self._check_extra_fields(**extra_fields):
            return self._create_user(username, email, password, False, **extra_fields)

    # def update_user(self, userid, **fields):
    #     """
    #     Updates user account details like username

    #     Note
    #     """
    #     try:

    #         if not fields["username"] or not fields["email"] or not fields["password"]:
    #             raise KeyError("No keys provided!")

    #         if fields["username"]:
    #             username = fields["username"]
    #             username_user = super().get_queryset().filter(username__exact=username)

    #             if username_user:
    #                 raise PreExistenceError(
    #                     username,
    #                     f'username "{username}" already taken. Try other username',
    #                 )

    #         if fields["email"]:
    #             email = fields["email"]
    #             if check_email_existence(email):
    #                 raise PreExistenceError(
    #                     email, f'username "{email}" already taken. Try other email'
    #                 )
    #             email_user = super().get_queryset().filter(email__exact=email)

    #         if username_user and email_user:
    #             if username_user.id != email_user.id:
    #                 raise UnmatchedFieldsError(
    #                     {"fields": [username, email]},
    #                     "Fields do not match! Given field values do not belong to same user!",
    #                 )

    #     except PreExistenceError as error:
    #         print(error)

    #     except UnmatchedFieldsError as error:
    #         print(error)


# TODO add logic to update_user
# NOTE cant use objects inside manager