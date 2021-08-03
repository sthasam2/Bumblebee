from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from bumblebee.buzzes.models import Buzz, Rebuzz
from bumblebee.comments.models import Comment
from bumblebee.profiles.models import Profile
from bumblebee.users.models import CustomUser

######################################
##           OWNER
######################################


class IsOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: CustomUser):
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


class IsCommentOwner(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj: Comment):
        """
        obj: Buzz instance
        """
        try:
            assert isinstance(obj, Comment), "`obj` must be an instance of model `Buzz`"

            return obj.commenter == request.user
        except AssertionError as error:
            print(error)
            raise error


######################################
##           PRIVACY
######################################
class IsBuzzPublic(BasePermission):
    def has_object_permission(self, request, view, obj: Buzz):
        """ """

        try:
            assert isinstance(obj, Buzz), "`obj` must be an instance of model `Buzz`"

            return obj.privacy == Buzz.PrivacyChoices.PUBLIC

        except AssertionError as error:
            print(error)
            raise error


class IsRebuzzPublic(BasePermission):
    def has_object_permission(self, request, view, obj: Rebuzz):
        """ """

        try:
            assert isinstance(obj, Rebuzz), "`obj` must be an instance of model `Buzz`"

            return obj.privacy == Rebuzz.PrivacyChoices.PUBLIC

        except AssertionError as error:
            print(error)
            raise error


class IsProfilePrivate(BasePermission):
    """ """

    def has_object_permission(self, request, view, obj):
        """ """

        return obj.private == True


######################################
##           MATCHING
######################################


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
