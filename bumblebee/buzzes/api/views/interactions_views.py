from rest_framework import status
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bumblebee.core.helpers import create_200, create_400, create_500
from bumblebee.buzzes.utils import (
    get_buzz_interaction_from_buzzid_or_raise,
    get_rebuzz_interaction_from_rebuzzid_or_raise,
)
from bumblebee.core.exceptions import NoneExistenceError, UrlParameterError
from bumblebee.core.permissions import IsBuzzPublic

# upvote
# downvote
# view TODO


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

            # check if already upvoted
            if userid not in buzz_interaction.upvotes:
                buzz_interaction.upvotes.append(userid)
                task = "Added UPVOTE"
            else:
                buzz_interaction.upvotes.remove(userid)
                task = "Removed DOWNVOTE"

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

            # check if already in downvoted
            if userid not in buzz_interaction.downvotes:
                buzz_interaction.downvotes.append(userid)
                task = "Added DOWNVOTE"
            else:
                buzz_interaction.downvotes.remove(userid)
                task = "Removed DOWNVOTE"

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

    permission_classes = [IsAuthenticated, IsBuzzPublic]

    def post(self, request, *args, **kwargs):
        """ """

        try:
            rebuzz_interaction = get_rebuzz_interaction_from_rebuzzid_or_raise(**kwargs)

            self.check_object_permissions(request, rebuzz_interaction.buzz)

            userid = request.user.id

            # check if already downvoted
            if userid in rebuzz_interaction.downvotes:
                rebuzz_interaction.downvotes.remove(userid)

            # check if already upvoted
            if userid not in rebuzz_interaction.upvotes:
                rebuzz_interaction.upvotes.append(userid)
                task = "Added UPVOTE"
            else:
                rebuzz_interaction.upvotes.remove(userid)
                task = "Removed DOWNVOTE"

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

    permission_classes = [IsAuthenticated, IsBuzzPublic]

    def post(self, request, *args, **kwargs):
        """ """

        try:
            rebuzz_interaction = get_rebuzz_interaction_from_rebuzzid_or_raise(**kwargs)
            self.check_object_permissions(request, rebuzz_interaction.buzz)
            userid = request.user.id

            # check if already upvoted
            if userid in rebuzz_interaction.upvotes:
                rebuzz_interaction.upvotes.remove(userid)

            # check if already in downvoted
            if userid not in rebuzz_interaction.downvotes:
                rebuzz_interaction.downvotes.append(userid)
                task = "Added DOWNVOTE"
            else:
                rebuzz_interaction.downvotes.remove(userid)
                task = "Removed DOWNVOTE"

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
