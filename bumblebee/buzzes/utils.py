from rest_framework import status

from bumblebee.buzzes.models import (
    Buzz,
    BuzzImage,
    BuzzInteractions,
    Rebuzz,
    RebuzzImage,
    RebuzzInteractions,
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
                    400,
                    "Non existence",
                    f"Buzz with id {url_buzzid} credentials does not exist!",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`buzzid` must be provided",
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
                    400,
                    "Non existence",
                    f"Buzz with id {url_buzzid} credentials does not exist!",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`buzzid` must be provided",
            ),
        )


def get_buzz_images_from_buzzid_or_raise(**kwargs):
    """ """

    url_buzzid = kwargs.get("buzzid")
    if url_buzzid:
        try:
            return BuzzImage.objects.filter(buzz__id=url_buzzid)

        except (TypeError, ValueError, OverflowError, Buzz.DoesNotExist):
            raise NoneExistenceError(
                url_buzzid,
                create_400(
                    400,
                    "Non existence",
                    f"Buzz with id {url_buzzid} credentials does not exist!",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`buzzid` must be provided",
            ),
        )


def get_rebuzz_from_rebuzzid_or_raise(**kwargs):
    """ """

    url_rebuzzid = kwargs.get("rebuzzid")
    if url_rebuzzid:
        try:
            return Rebuzz.objects.get(id=url_rebuzzid)

        except (TypeError, ValueError, OverflowError, Buzz.DoesNotExist):
            raise NoneExistenceError(
                url_rebuzzid,
                create_400(
                    400,
                    "Non existence",
                    f"Rebuzz with id {url_rebuzzid} credentials does not exist!",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`buzzid` must be provided",
            ),
        )


def get_rebuzz_interaction_from_rebuzzid_or_raise(**kwargs):
    """ """

    url_rebuzzid = kwargs.get("rebuzzid")
    if url_rebuzzid:
        try:
            return RebuzzInteractions.objects.get(rebuzz__id=url_rebuzzid)

        except (TypeError, ValueError, OverflowError, Buzz.DoesNotExist):
            raise NoneExistenceError(
                url_rebuzzid,
                create_400(
                    400,
                    "Non existence",
                    f"Rebuzz with id {url_rebuzzid} credentials does not exist!",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`rebuzzid` must be provided",
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
                    400,
                    "Non existence",
                    f"Rebuzz with id {url_rebuzzid} credentials does not exist!",
                ),
            )
    else:
        raise UrlParameterError(
            instance="Url Buzzid",
            message=create_400(
                status.HTTP_400_BAD_REQUEST,
                "Url parameter wrong",
                "`rebuzzid` must be provided",
            ),
        )
