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
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path(
        "dashboard/cms/hitlist",
        views.HistListListView.as_view(),
        name="hitlist-list",
    ),
    path(
        "dashboard/cms/hitlist/create",
        views.HitListCreateView.as_view(),
        name="hitlist-create",
    ),
    path(
        "dashboard/cms/hitlist/update/<str:pk>",
        views.HitListUpdateView.as_view(),
        name="hitlist-update",
    ),
    path(
        "dashboard/cms/hitlist/delete/<str:pk>",
        views.HitListDeleteView.as_view(),
        name="hitlist-delete",
    ),
]
