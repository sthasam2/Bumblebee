from rest_framework.permissions import BasePermission

from bumblebee.users.models import CustomUser
from bumblebee.profiles.models import Profile


class IsOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj):
        """ """

        return obj == request.user


class IsProfileOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj):
        """ """

        return obj.user == request.user


class IsBuzzOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj):
        """
        obj: Buzz instance
        """

        return obj.author == request.user


class IsProfilePrivate(BasePermission):
    """ """

    def has_object_permission(self, obj):
        """ """

        return obj.private == True


class IsPasswordMatching(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: CustomUser):
        """ """

        return obj.check_password(request.data.get("current_password"))


class IsProfilePasswordMatching(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: Profile):
        """ """

        return obj.user.check_password(request.data.get("current_password"))
