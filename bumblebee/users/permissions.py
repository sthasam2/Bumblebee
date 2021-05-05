from rest_framework.permissions import BasePermission

from bumblebee.users.models import CustomUser


class IsOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj):
        """ """

        return obj == request.user


class IsPasswordMatching(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: CustomUser):
        """ """

        return obj.check_password(request.data.get("current_password"))
