from django.urls import path

from bumblebee.notifications.api.views.grouped_notification_views import (
    UserGroupedNotificationListView,
    UserGroupedNotificationView,
)
from bumblebee.notifications.api.views.individual_notification_views import (
    UserIndividualNotificationListView,
    UserIndividualNotificationView,
)

urlpatterns = [
    path(
        "grouped/categorized",
        UserGroupedNotificationView.as_view(),
        name="user-notifications-categorized",
    ),
    path(
        "grouped/list",
        UserGroupedNotificationListView.as_view(),
        name="user-notifications-list",
    ),
    path(
        "individual/categorized",
        UserIndividualNotificationView.as_view(),
        name="user-notifications-categorized",
    ),
    path(
        "individual/list",
        UserIndividualNotificationListView.as_view(),
        name="user-notifications-list",
    ),
]
