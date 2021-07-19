from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.core.exceptions import (
    MissingFieldsError,
    NoneExistenceError,
    UrlParameterError,
)
from bumblebee.core.helpers import create_200, create_400, create_500
from bumblebee.core.permissions import IsOwner
from bumblebee.users.utils import DbExistenceChecker
from bumblebee.users.models import CustomUser
from bumblebee.connections.api.serializers.connection_serializers import (
    BlockedSerializer,
    FollowerSerializer,
    FollowingSerializer,
    MutedSerializer,
)
from bumblebee.connections.api.serializers.connection_users_serializers import (
    ConnectionUserSerializer,
)

######################################
##           RETRIEVE
######################################


class RetrieveConnectionListView(APIView):
    """ """

    permission_classes = [AllowAny]

    def _get_connections(self, *args, **kwargs):
        """ """
        connectionid_list = self.request.data.get("connection_userid_list", False)

        if connectionid_list:
            connections = CustomUser.objects.filter(id__in=connectionid_list)
            return dict(
                connections=connections.all(),
                non_existing=(
                    set(connectionid_list)
                    - set([buzz.id for buzz in connections.all()])
                ),
            )
        else:
            raise MissingFieldsError(
                "buzzid_list",
                create_400(
                    400,
                    "Missing Fields",
                    "Request body must contain field `connection_userid_list`",
                ),
            )

    def post(self, request, *args, **kwargs):
        """ """

        try:

            connection_instances = self._get_connections()
            connection_serializer = ConnectionUserSerializer(
                connection_instances["connections"], many=True
            )

            return Response(
                data=dict(
                    connections=connection_serializer.data,
                    non_existing=connection_instances["non_existing"],
                ),
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not get connection users for `connection_userid_list` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveUserConnectionListView(APIView):
    """ """

    permission_classes = [AllowAny]

    def _get_url_user(self):
        """ """
        url_username = self.kwargs.get("username", False)

        if url_username:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=url_username
            )

            if user_instance.profile.private:
                raise PermissionDenied(
                    detail="Private Profile",
                    code="User has made their profile private.",
                )

            return user_instance
        else:
            raise UrlParameterError(
                "username",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `username`",
                ),
            )

    def _get_followers_from_idlist(self, connectionid_list, *args, **kwargs):
        """ """
        return CustomUser.objects.filter(id__in=connectionid_list)

    def get(self, request, *args, **kwargs):
        """ """

        try:
            user_instance = self._get_url_user()
            follower = self._get_followers_from_idlist(
                connectionid_list=user_instance.user_follower.follower
            )
            following = self._get_followers_from_idlist(
                connectionid_list=user_instance.user_following.following
            )

            follower_serializer = ConnectionUserSerializer(follower, many=True)
            following_serializer = ConnectionUserSerializer(following, many=True)

            if user_instance == self.request.user:
                muted = self._get_followers_from_idlist(
                    connectionid_list=user_instance.user_muted.muted
                )
                blocked = self._get_followers_from_idlist(
                    connectionid_list=user_instance.user_blocked.blocked
                )
                muted_serializer = ConnectionUserSerializer(muted, many=True)
                blocked_serializer = ConnectionUserSerializer(blocked, many=True)

                return Response(
                    data=dict(
                        follower=follower_serializer.data,
                        following=following_serializer.data,
                        muted=muted_serializer.data,
                        blocked=blocked_serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    data=dict(
                        follower=follower_serializer.data,
                        following=following_serializer.data,
                    ),
                    status=status.HTTP_200_OK,
                )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not get connection users for `connection_userid_list` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveFollowerListView(APIView):
    """ """

    permission_classes = [AllowAny]

    def _get_url_user(self):
        """ """
        url_username = self.kwargs.get("username", False)

        if url_username:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=url_username
            )

            if user_instance.profile.private:
                raise PermissionDenied(
                    detail="Private Profile",
                    code="User has made their profile private.",
                )

            return user_instance
        else:
            raise UrlParameterError(
                "username",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `username`",
                ),
            )

    def get(self, request, *args, **kwargs):
        """ """

        try:
            user_instance = self._get_url_user()
            follower_serializer = FollowerSerializer(
                user_instance.user_follower, many=False
            )
            # followers = user_instance.user_follower.follower
            # connection_serializer = ConnectionUserSerializer(followers, many=True)

            return Response(
                follower_serializer.data,
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not get followers of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveFollowingListView(APIView):
    """ """

    permission_classes = [AllowAny]

    def _get_url_user(self):
        """ """
        url_username = self.kwargs.get("username", False)

        if url_username:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=url_username
            )

            if user_instance.profile.private:
                raise PermissionDenied(
                    detail="Private Profile",
                    code="User has made their profile private.",
                )

            return user_instance
        else:
            raise UrlParameterError(
                "username",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `username`",
                ),
            )

    def get(self, request, *args, **kwargs):
        """ """

        try:
            user_instance = self._get_url_user()
            following_serializer = FollowingSerializer(
                user_instance.user_following, many=False
            )

            return Response(
                following_serializer.data,
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not get following of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveMutedIDListView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ """

        try:
            user_instance = self.request.user
            self.check_object_permissions(request, user_instance)
            muted_serializer = MutedSerializer(user_instance.user_muted, many=False)

            return Response(
                muted_serializer.data,
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not get muted accounts of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RetrieveBlockedIDListView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """ """

        try:
            user_instance = self.request.user

            blocked_serializer = BlockedSerializer(
                user_instance.user_blocked, many=False
            )

            return Response(
                blocked_serializer.data,
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not get blocked accounts of `{kwargs.get('username')}` due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


######################################
##           CREATE
######################################


class AcceptFollowRequestView(APIView):
    """ """

    permission_classes = [IsAuthenticated, IsOwner]

    def _get_user_to_accept(self):
        """ """
        username_to_accept = self.request.data.get("username", False)

        if username_to_accept:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_accept
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Missing Fields",
                    "re body must contain `username`",
                ),
            )

    def post(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user

            user_to_accept = self._get_user_to_accept()

            if user_to_accept.id in owner_user.user_follower.requests_for_follow:
                owner_user.user_follower.follower.append(user_to_accept.id)
                owner_user.user_follower.requests_for_follow.remove(user_to_accept.id)

                user_to_accept.user_following.following.append(owner_user.id)
                user_to_accept.user_following.requesting_to_follow.remove(owner_user.id)

            owner_user.user_follower.save()
            user_to_accept.user_following.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    "follow",
                    f"Successfully accepted @{user_to_accept.username}",
                ),
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not follow due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class FollowUnfollowRequestUnrequestView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_user_to_follow_unfollow(self):
        """ """
        username_to_follow_unfollow = self.request.data.get("username", False)

        if username_to_follow_unfollow:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_follow_unfollow
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Missing Fields",
                    "req body must contain `username`",
                ),
            )

    def post(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user
            user_to_follow_unfollow = self._get_user_to_follow_unfollow()

            task = None

            #  if follow unfollow
            if user_to_follow_unfollow.id in owner_user.user_following.following:
                owner_user.user_following.following.remove(user_to_follow_unfollow.id)
                user_to_follow_unfollow.user_follower.follower.remove(owner_user.id)
                task = "Unfollow"

            #  if not private and not followed follow
            elif not user_to_follow_unfollow.profile.private:
                # if not followed follow
                if (
                    user_to_follow_unfollow.id
                    not in owner_user.user_following.following
                ):
                    user_to_follow_unfollow.user_follower.follower.append(owner_user.id)
                    owner_user.user_following.following.append(
                        user_to_follow_unfollow.id
                    )
                    task = "Follow"

            # If private create request
            elif user_to_follow_unfollow.profile.private:
                if (
                    owner_user.id
                    not in user_to_follow_unfollow.user_follower.requests_for_follow
                ):
                    user_to_follow_unfollow.user_follower.requests_for_follow.append(
                        owner_user.id
                    )
                    owner_user.user_following.requesting_to_follow.append(
                        user_to_follow_unfollow.id
                    )
                    task = "Request Follow"

                elif (
                    owner_user.id
                    in user_to_follow_unfollow.user_follower.requests_for_follow
                ):
                    user_to_follow_unfollow.user_follower.requests_for_follow.remove(
                        owner_user.id
                    )
                    owner_user.user_following.requesting_to_follow.remove(
                        user_to_follow_unfollow.id
                    )
                    task = "Cancel Request Follow"

            user_to_follow_unfollow.user_follower.save()
            user_to_follow_unfollow.user_following.save()
            owner_user.user_follower.save()
            owner_user.user_following.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"Successfully {task} @{user_to_follow_unfollow.username}",
                ),
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not {task} due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class MuteUnmuteView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_user_to_mute_unmute(self):
        """ """
        username_to_mute_unmute = self.request.data.get("username", False)

        if username_to_mute_unmute:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_mute_unmute
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Missing Fields",
                    "req body must contain `username`",
                ),
            )

    def post(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user
            user_to_mute_unmute = self._get_user_to_mute_unmute()
            task = None

            if user_to_mute_unmute not in owner_user.user_muted.muted:
                owner_user.user_muted.muted.append(user_to_mute_unmute.id)
                task = "Mute"

            elif user_to_mute_unmute in owner_user.user_muted.muted:
                owner_user.user_muted.muted.remove(user_to_mute_unmute.id)
                task = "Unmute"

            owner_user.user_muted.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"Successfully {task} @{user_to_mute_unmute.username}",
                ),
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not mute due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class BlockUnblockView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_user_to_block_unblock(self):
        """ """
        username_to_block_unblock = self.request.data.get("username", False)

        if username_to_block_unblock:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_block_unblock
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Url Error",
                    "Url must contain `username`",
                ),
            )

    def post(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user
            user_to_block_unblock = self._get_user_to_block_unblock()

            if user_to_block_unblock.id not in owner_user.user_blocked.blocked:
                owner_user.user_blocked.blocked.append(user_to_block_unblock.id)
                task = "Block"

            elif user_to_block_unblock.id in owner_user.user_blocked.blocked:
                owner_user.user_blocked.blocked.remove(user_to_block_unblock.id)
                task = "Unblock"

            owner_user.user_blocked.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"Successfully {task} @{user_to_block_unblock.username}",
                ),
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not mute due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


######################################
##           DELETE
######################################


class DeleteFollowRequestView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_user_to_reject(self):
        """ """
        username_to_reject = self.request.data.get("username", False)

        if username_to_reject:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_reject
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Missing Fields",
                    "req body must contain `username`",
                ),
            )

    def delete(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user
            user_to_reject = self._get_user_to_reject()

            if user_to_reject.id in owner_user.user_follower.requests_for_follow:
                owner_user.user_follower.request_for_follow.remove(user_to_reject.id)
                user_to_reject.user_following.requesting_to_follow.remove(owner_user.id)

                owner_user.user_follower.save()
                user_to_reject.user_following.save()

                return Response(
                    data=create_200(
                        status.HTTP_200_OK,
                        "follow",
                        f"Successfully accepted @{user_to_reject.username}",
                    ),
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    data=create_200(
                        status.HTTP_200_OK,
                        "no request for follow",
                        f"User @{user_to_reject.username} has not requested to follow you.",
                    ),
                    status=status.HTTP_200_OK,
                )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not remove follow request due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteFollowerView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_user_to_remove_follow(self):
        """ """
        username_to_remove_follow = self.request.data.get("username", False)

        if username_to_remove_follow:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_remove_follow
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Missing Fields",
                    "req body must contain `username`",
                ),
            )

    def delete(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user
            user_to_remove_follow = self._get_user_to_remove_follow()

            if user_to_remove_follow.id in owner_user.user_follower.follower:
                owner_user.user_follower.follower.remove(user_to_remove_follow.id)
                user_to_remove_follow.user_following.following.remove(owner_user.id)

                owner_user.user_follower.save()
                user_to_remove_follow.user_following.save()

                return Response(
                    data=create_200(
                        status.HTTP_200_OK,
                        "follow",
                        f"Successfully removed follower @{user_to_remove_follow.username}",
                    ),
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    data=create_200(
                        status.HTTP_200_OK,
                        "not following",
                        f"User @{user_to_remove_follow.username} is not following you.",
                    ),
                    status=status.HTTP_200_OK,
                )
        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not follow due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteFollowingView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_user_to_follow(self):
        """ """
        username_to_remove_follow = self.request.data.get("username", False)

        if username_to_remove_follow:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_remove_follow
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Missing Fields",
                    "req body must contain `username`",
                ),
            )

    def delete(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user
            user_to_remove_following = self._get_user_to_remove_following()

            owner_user.user_following.following.remove(user_to_remove_following.id)
            user_to_remove_following.user_follower.follower.remove(owner_user.id)

            owner_user.user_following.save()
            user_to_remove_following.user_follower.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    "follow",
                    f"Successfully removed follower @{user_to_remove_following.username}",
                ),
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not follow due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteMutedView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_user_to_umute(self):
        """ """
        username_to_mute = self.request.data.get("username", False)

        if username_to_mute:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_mute
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Missing Fields",
                    "req body must contain `username`",
                ),
            )

    def delete(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user
            user_to_unmute = self._get_user_to_unmute()

            if user_to_unmute.id in owner_user.user_muted.muted:
                owner_user.user_muted.muted.remove(user_to_unmute.id)
                owner_user.user_muted.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    "follow",
                    f"Successfully unmuted @{user_to_unmute.username}",
                ),
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not mute due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteBlockedView(APIView):
    """ """

    permission_classes = [IsAuthenticated]

    def _get_user_to_unblock(self):
        """ """
        username_to_unblock = self.request.data.get("username", False)

        if username_to_unblock:
            user_instance = DbExistenceChecker().check_return_user_existence(
                username=username_to_unblock
            )

            return user_instance
        else:
            raise MissingFieldsError(
                "username",
                create_400(
                    400,
                    "Missing Fields",
                    "req body must contain `username`",
                ),
            )

    def post(self, *args, **kwargs):
        """ """
        try:
            owner_user = self.request.user
            user_to_unblock = self._get_user_to_unblock()

            if user_to_unblock.id in owner_user.user_blocked.blocked:
                owner_user.user_muted.muted.remove(user_to_unblock.id)
                owner_user.user_muted.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    "follow",
                    f"Successfully blocked @{user_to_unblock.username}",
                ),
                status=status.HTTP_200_OK,
            )

        except (MissingFieldsError, UrlParameterError, NoneExistenceError) as error:
            return Response(error.message, status=error.message.get("status"))

        except (PermissionDenied, NotAuthenticated) as error:
            return Response(
                create_400(
                    error.status_code,
                    error.get_codes(),
                    error.get_full_details().get("message"),
                ),
                status=error.status_code,
            )

        except Exception as error:
            return Response(
                create_500(
                    cause=error.args[0] or None,
                    verbose=f"Could not mute due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
