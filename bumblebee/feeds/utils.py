import datetime as dt
import random

import pytz
from django.db.models import Q

from bumblebee.buzzes.models import Buzz, Rebuzz
from bumblebee.users.models import CustomUser
from config.definitions import TIME_ZONE


def select_max_10_random(ids_list):
    """ """
    random_ids = set()
    for i in range(0, 10):
        choice = random.choice(ids_list)
        random_ids.add(choice)
    return list(random_ids)


def get_date_a_week_ago():
    """Get the date a week ago"""

    weekago = pytz.timezone(TIME_ZONE).localize(dt.datetime.utcnow()) - dt.timedelta(
        days=7
    )
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


def get_follow_suggestions_for_user(owner_user):
    """Get followings of an authentucated user's followings to suggest"""

    following_ids = owner_user.user_following.following
    blacklist_ids = owner_user.user_muted.muted + owner_user.user_blocked.blocked

    ids_to_exclude = following_ids + blacklist_ids + [owner_user.id]

    rec_ids = []
    for account in CustomUser.objects.filter(id__in=following_ids):
        rec_ids += account.user_following.following

    filtered_ids = list(set(rec_ids) - set(ids_to_exclude))

    if len(filtered_ids) >= 10:
        return CustomUser.objects.filter(id__in=select_max_10_random(filtered_ids))[:10]

    elif len(filtered_ids) > 0:
        return CustomUser.objects.filter(id__in=filtered_ids)

    else:
        return CustomUser.objects.exclude(id__in=ids_to_exclude)[:10]
