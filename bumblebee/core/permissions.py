from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from bumblebee.users.models import CustomUser
from bumblebee.profiles.models import Profile
from bumblebee.buzzes.models import Buzz, Rebuzz


class IsOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj):
        """ """

        is_owner = obj == request.user
        if is_owner:
            return is_owner
        else:
            raise PermissionDenied(
                detail="Request user is not an instance of Targeted user. Permission Denied",
                code="Permission Denied!",
            )


class IsProfileOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: Profile):
        """ """

        return obj.user == request.user


class IsBuzzPublic(BasePermission):
    def has_object_permission(self, request, view, obj: Buzz):
        """ """

        try:
            assert isinstance(obj, Buzz), "`obj` must be an instance of model `Buzz`"

            return obj.privacy == Buzz.PrivacyChoices.PUBLIC

        except AssertionError as error:
            print(error)
            raise error


class IsBuzzOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: Buzz):
        """
        obj: Buzz instance
        """
        try:
            assert isinstance(obj, Buzz), "`obj` must be an instance of model `Buzz`"

            return obj.author == request.user
        except AssertionError as error:
            print(error)
            raise error


class IsRebuzzOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: Rebuzz):
        """
        obj: Buzz instance
        """
        try:
            assert isinstance(
                obj, Rebuzz
            ), "`obj` must be an instance of model `Rebuzz`"

            return obj.author == request.user
        except AssertionError as error:
            print(error)
            raise error


class IsProfilePrivate(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj):
        """ """

        return obj.private == True


class IsPasswordMatching(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: CustomUser):
        """ """

        password_matching = obj.check_password(request.data.get("current_password"))
        if password_matching:
            return password_matching
        else:
            raise PermissionDenied(
                detail="Password incorrect. Please enter correct password",
                code="Permission Denied!",
            )


class IsProfilePasswordMatching(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: Profile):
        """ """

        return obj.user.check_password(request.data.get("current_password"))
