from django.db.models import Q

import datetime as dt

from bumblebee.buzzes.models import Buzz, Rebuzz


def get_date_a_week_ago():
    """Get the date a week ago"""

    today = dt.datetime.now()
    weekago = today - dt.timedelta(days=7)
    return weekago


def get_folowing_buzzes_for_user(owner_user):
    """Get buzzes of an authentucated user followings"""

    ids_to_use = owner_user.user_following.following
    blacklist_ids = owner_user.user_muted.muted + owner_user.user_blocked.blocked
    date_limit = get_date_a_week_ago()

    buzzes = (
        Buzz.objects.filter(Q(author__in=ids_to_use) & Q(created_date__gte=date_limit))
        .exclude(author__in=blacklist_ids)
        .order_by("-created_date")
    )
    rebuzzes = (
        Rebuzz.objects.filter(
            Q(author__in=ids_to_use) & Q(created_date__gte=date_limit)
        )
        .exclude(author__in=blacklist_ids)
        .order_by("-created_date")
    )

    return dict(buzzes=buzzes.all(), rebuzzes=rebuzzes.all())
