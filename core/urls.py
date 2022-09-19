from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("stemmen/", views.VoteView.as_view(), name="vote"),
    path(
        "stem/<uuid:pk>",
        views.VoteSubmissionDetailView.as_view(),
        name="vote-submission-detail",
    ),
    path("api/search/", views.SpotipySearchView.as_view(), name="api-search"),
    path(
        "api/get/<str:spotifyuri>",
        views.SpotipyGetView.as_view(),
        name="api-get",
    ),
]
