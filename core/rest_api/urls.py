from django.urls import path, include
from rest_framework import routers

import core.rest_api.views as views

router = routers.SimpleRouter()

app_name = "api"

urlpatterns = [
    path("", include(router.urls)),
    path(
        "current_hitlist/",
        views.CurrentHitListView.as_view(),
        name="current-hitlist",
    ),
    path("api/search/", views.SpotipySearchView.as_view(), name="search"),
    path(
        "api/get/<str:spotifyuri>",
        views.SpotipyGetView.as_view(),
        name="get",
    ),
    path("api/stats/", views.TrackStatsGetView.as_view(), name="track-stats"),
]
