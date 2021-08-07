from django.urls import re_path

from bumblebee.search.api.views.search_views import SearchView

urlpatterns = [
    #     re_path(
    #         r"(?:keyword=(?P<keyword>\d+)&username=(?P<username>\d+))?$",
    #         SearchView.as_view(),
    #     ),
    re_path(
        r"list(?:keyword=(?P<keyword>\d+))?$",
        SearchView.as_view(),
    ),
]
