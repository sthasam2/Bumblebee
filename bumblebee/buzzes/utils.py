from django.db.models import Q
from rest_framework import status

from bumblebee.buzzes.models import (
    Buzz,
    BuzzImage,
    BuzzInteractions,
    BuzzUpvoteDownvoteMeta,
    Rebuzz,
    RebuzzImage,
    RebuzzInteractions,
    RebuzzUpvoteDownvoteMeta,
)
from bumblebee.core.exceptions import NoneExistenceError, UrlParameterError
from bumblebee.core.helpers import create_400


def get_buzz_from_buzzid_or_raise(**kwargs):
    """ """

    url_buzzid = kwargs.get("buzzid")
    if url_buzzid:
        try:
            return Buzz.objects.get(id=url_buzzid)

        except (TypeError, ValueError, OverflowError, Buzz.DoesNotExist):
            raise NoneExistenceError(
                url_buzzid,
                create_400(
                    404,
                    "Non existence",
                    f"Buzz with id {url_buzzid} credentials does not exist!",
                    "buzz",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`buzzid` must be provided",
                "url:buzzid",
            ),
        )


def get_buzz_interaction_from_buzzid_or_raise(**kwargs):
    """ """

    url_buzzid = kwargs.get("buzzid")
    if url_buzzid:
        try:
            return BuzzInteractions.objects.get(buzz__id=url_buzzid)

        except (TypeError, ValueError, OverflowError, BuzzInteractions.DoesNotExist):
            raise NoneExistenceError(
                url_buzzid,
                create_400(
                    404,
                    "Non existence",
                    f"Buzz with id {url_buzzid} credentials does not exist!",
                    "buzz",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`buzzid` must be provided",
                "url:buzzid",
            ),
        )


def get_buzz_images_from_buzzid_or_raise(**kwargs):
    """ """

    url_buzzid = kwargs.get("buzzid")
    if url_buzzid:
        try:
            return BuzzImage.objects.filter(buzz__id=url_buzzid)

        except (TypeError, ValueError, OverflowError, BuzzImage.DoesNotExist):
            raise NoneExistenceError(
                url_buzzid,
                create_400(
                    404,
                    "Non existence",
                    f"Buzz with id {url_buzzid} credentials does not exist!",
                    "buzz",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`buzzid` must be provided",
                "url:buzzid",
            ),
        )


def get_rebuzz_from_rebuzzid_or_raise(**kwargs):
    """ """

    url_rebuzzid = kwargs.get("rebuzzid")
    if url_rebuzzid:
        try:
            return Rebuzz.objects.get(id=url_rebuzzid)

        except (TypeError, ValueError, OverflowError, Rebuzz.DoesNotExist):
            raise NoneExistenceError(
                url_rebuzzid,
                create_400(
                    404,
                    "Non existence",
                    f"Rebuzz with id {url_rebuzzid} credentials does not exist!",
                    "rebuzz",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`buzzid` must be provided",
                "url:buzzid",
            ),
        )


def get_rebuzz_interaction_from_rebuzzid_or_raise(**kwargs):
    """ """

    url_rebuzzid = kwargs.get("rebuzzid")
    if url_rebuzzid:
        try:
            return RebuzzInteractions.objects.get(rebuzz__id=url_rebuzzid)

        except (TypeError, ValueError, OverflowError, RebuzzInteractions.DoesNotExist):
            raise NoneExistenceError(
                url_rebuzzid,
                create_400(
                    404,
                    "Non existence",
                    f"Rebuzz with id {url_rebuzzid} credentials does not exist!",
                    "rebuzz",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`rebuzzid` must be provided",
                "url:rebuzzid",
            ),
        )


def get_rebuzz_images_from_rebuzzid_or_raise(**kwargs):
    """ """

    url_rebuzzid = kwargs.get("rebuzzid")
    if url_rebuzzid:
        try:
            return RebuzzImage.objects.filter(rebuzz__id=url_rebuzzid)

        except (TypeError, ValueError, OverflowError, Buzz.DoesNotExist):
            raise NoneExistenceError(
                url_rebuzzid,
                create_400(
                    404,
                    "Non existence",
                    f"Rebuzz with id {url_rebuzzid} credentials does not exist!",
                    "rebuzz",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`rebuzzid` must be provided",
                "url:rebuzzid",
            ),
        )


# Interaction Meta


def create_buzz_upvdwv_meta(comment_interaction, userid, action):
    """ """

    if action == "UPV":
        BuzzUpvoteDownvoteMeta.objects.create(
            comment_interaction=comment_interaction,
            userid=userid,
            action=BuzzUpvoteDownvoteMeta.ActionChoices.UPVOTE,
        )
    elif action == "DWV":
        BuzzUpvoteDownvoteMeta.objects.create(
            comment_interaction=comment_interaction,
            userid=userid,
            action=BuzzUpvoteDownvoteMeta.ActionChoices.DOWNVOTE,
        )


def delete_buzz_upvdwv_meta(comment_interaction, userid, action):
    """ """

    if action == "UPV":
        BuzzUpvoteDownvoteMeta.objects.get(
            Q(comment_interaction=comment_interaction),
            Q(userid=userid),
            Q(action=BuzzUpvoteDownvoteMeta.ActionChoices.UPVOTE),
        ).delete()
    elif action == "DWV":
        BuzzUpvoteDownvoteMeta.objects.get(
            Q(comment_interaction=comment_interaction),
            Q(userid=userid),
            Q(action=BuzzUpvoteDownvoteMeta.ActionChoices.DOWNVOTE),
        ).delete()


def create_rebuzz_upvdwv_meta(comment_interaction, userid, action):
    """ """

    if action == "UPV":
        RebuzzUpvoteDownvoteMeta.objects.create(
            comment_interaction=comment_interaction,
            userid=userid,
            action=RebuzzUpvoteDownvoteMeta.ActionChoices.UPVOTE,
        )
    elif action == "DWV":
        RebuzzUpvoteDownvoteMeta.objects.create(
            comment_interaction=comment_interaction,
            userid=userid,
            action=RebuzzUpvoteDownvoteMeta.ActionChoices.DOWNVOTE,
        )


def delete_buzz_upvdwv_meta(comment_interaction, userid, action):
    """ """

    if action == "UPV":
        RebuzzUpvoteDownvoteMeta.objects.get(
            Q(comment_interaction=comment_interaction),
            Q(userid=userid),
            Q(action=RebuzzUpvoteDownvoteMeta.ActionChoices.UPVOTE),
        ).delete()
    elif action == "DWV":
        RebuzzUpvoteDownvoteMeta.objects.get(
            Q(comment_interaction=comment_interaction),
            Q(userid=userid),
            Q(action=RebuzzUpvoteDownvoteMeta.ActionChoices.DOWNVOTE),
        ).delete()


def check_previously_rebuzzed(user, buzzid):
    """ """

    exists = Rebuzz.objects.get(Q(author__id=user.id), Q(buzz_id=buzzid)).exists()
