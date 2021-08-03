from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.buzzes.utils import (
    get_buzz_interaction_from_buzzid_or_raise,
    get_rebuzz_interaction_from_rebuzzid_or_raise,
)
from bumblebee.core.exceptions import (
    NoneExistenceError,
    NotAuthenticated,
    PermissionDenied,
    UrlParameterError,
)
from bumblebee.core.helpers import create_200, create_400, create_500
from bumblebee.core.permissions import IsBuzzPublic, IsRebuzzPublic
from bumblebee.notifications.choices import ACTION_TYPE, CONTENT_TYPE
from bumblebee.notifications.utils import create_notification, delete_notification

########################################
##              BUZZ
########################################


class UpvoteBuzzView(APIView):
    """
    Upvote a given buzz
    """

    permission_classes = [IsAuthenticated, IsBuzzPublic]

    def post(self, request, *args, **kwargs):
        """ """

        try:
            buzz_interaction = get_buzz_interaction_from_buzzid_or_raise(**kwargs)

            self.check_object_permissions(request, buzz_interaction.buzz)

            userid = request.user.id

            # check if already downvoted
            if userid in buzz_interaction.downvotes:
                buzz_interaction.downvotes.remove(userid)

                delete_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["BUZZ"],
                    request.user,
                    buzz_interaction.buzz,
                )
            # check if already upvoted
            if userid not in buzz_interaction.upvotes:
                buzz_interaction.upvotes.append(userid)
                task = "Added UPVOTE"

                create_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["BUZZ"],
                    request.user,
                    buzz_interaction.buzz,
                )
            else:
                buzz_interaction.upvotes.remove(userid)
                task = "Removed UPVOTE"

                delete_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["BUZZ"],
                    request.user,
                    buzz_interaction.buzz,
                )

            buzz_interaction.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"{task} on post {{ id:{buzz_interaction.buzz.id}, author:{buzz_interaction.buzz.author.username} }}",
                ),
                status=status.HTTP_200_OK,
            )
        except (UrlParameterError, NoneExistenceError) as error:
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
                    verbose=f"Could not upvote due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DownvoteBuzzView(APIView):
    """ """

    permission_classes = [IsAuthenticated, IsBuzzPublic]

    def post(self, request, *args, **kwargs):
        """ """

        try:
            buzz_interaction = get_buzz_interaction_from_buzzid_or_raise(**kwargs)
            self.check_object_permissions(request, buzz_interaction.buzz)
            userid = request.user.id

            # check if already upvoted
            if userid in buzz_interaction.upvotes:
                buzz_interaction.upvotes.remove(userid)

                delete_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["BUZZ"],
                    request.user,
                    buzz_interaction.buzz,
                )

            # check if already in downvoted
            if userid not in buzz_interaction.downvotes:
                buzz_interaction.downvotes.append(userid)
                task = "Added DOWNVOTE"

                create_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["BUZZ"],
                    request.user,
                    buzz_interaction.buzz,
                )

            else:
                buzz_interaction.downvotes.remove(userid)
                task = "Removed DOWNVOTE"

                delete_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["BUZZ"],
                    request.user,
                    buzz_interaction.buzz,
                )

            buzz_interaction.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"{task} on post {{ id:{buzz_interaction.buzz.id}, author:{buzz_interaction.buzz.author.username} }}",
                ),
                status=status.HTTP_200_OK,
            )
        except (UrlParameterError, NoneExistenceError) as error:
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
                    verbose=f"Could not downvote due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


########################################
##              REBUZZ
########################################
class UpvoteRebuzzView(APIView):
    """ """

    permission_classes = [IsAuthenticated, IsRebuzzPublic]

    def post(self, request, *args, **kwargs):
        """ """

        try:
            rebuzz_interaction = get_rebuzz_interaction_from_rebuzzid_or_raise(**kwargs)

            self.check_object_permissions(request, rebuzz_interaction.rebuzz)

            userid = request.user.id

            # check if already downvoted
            if userid in rebuzz_interaction.downvotes:
                rebuzz_interaction.downvotes.remove(userid)

                delete_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["RBZ"],
                    request.user,
                    rebuzz_interaction.rebuzz,
                )

            # check if already upvoted
            if userid not in rebuzz_interaction.upvotes:
                rebuzz_interaction.upvotes.append(userid)
                task = "Added UPVOTE"

                create_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["RBZ"],
                    request.user,
                    rebuzz_interaction.rebuzz,
                )

            else:
                rebuzz_interaction.upvotes.remove(userid)
                task = "Removed DOWNVOTE"

                delete_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["RBZ"],
                    request.user,
                    rebuzz_interaction.rebuzz,
                )

            rebuzz_interaction.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"{task} on post {{ id:{rebuzz_interaction.rebuzz.id}, author:{rebuzz_interaction.rebuzz.author.username} }}",
                ),
                status=status.HTTP_200_OK,
            )
        except (UrlParameterError, NoneExistenceError) as error:
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
                    verbose=f"Could not upvote due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DownvoteRebuzzView(APIView):
    """ """

    permission_classes = [IsAuthenticated, IsRebuzzPublic]

    def post(self, request, *args, **kwargs):
        """ """

        try:
            rebuzz_interaction = get_rebuzz_interaction_from_rebuzzid_or_raise(**kwargs)
            self.check_object_permissions(request, rebuzz_interaction.rebuzz)
            userid = request.user.id

            # check if already upvoted
            if userid in rebuzz_interaction.upvotes:
                rebuzz_interaction.upvotes.remove(userid)

                delete_notification(
                    ACTION_TYPE["UPV"],
                    CONTENT_TYPE["RBZ"],
                    request.user,
                    rebuzz_interaction.rebuzz,
                )

            # check if already in downvoted
            if userid not in rebuzz_interaction.downvotes:
                rebuzz_interaction.downvotes.append(userid)
                task = "Added DOWNVOTE"

                create_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["RBZ"],
                    request.user,
                    rebuzz_interaction.rebuzz,
                )
            else:
                rebuzz_interaction.downvotes.remove(userid)
                task = "Removed DOWNVOTE"

                delete_notification(
                    ACTION_TYPE["DWV"],
                    CONTENT_TYPE["RBZ"],
                    request.user,
                    rebuzz_interaction.rebuzz,
                )
            rebuzz_interaction.save()

            return Response(
                data=create_200(
                    status.HTTP_200_OK,
                    task,
                    f"{task} on post {{ id:{rebuzz_interaction.rebuzz.id}, author:{rebuzz_interaction.rebuzz.author.username} }}",
                ),
                status=status.HTTP_200_OK,
            )
        except (UrlParameterError, NoneExistenceError) as error:
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
                    verbose=f"Could not downvote due to an unknown error",
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# FIXME create decorators for exception cases
