from django.urls import path

from . import views


app_name = "core"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("closed/", views.HitlistClosedView.as_view(), name="closed"),
    path("stemmen/", views.VoteView.as_view(), name="vote"),
    path(
        "stem/<uuid:pk>",
        views.VoteSubmissionDetailView.as_view(),
        name="vote-submission-detail",
    ),
    path(
        "eigen-nummer-toegevoegen/",
        views.AddCustomTrackView.as_view(),
        name="add-custom-track",
    ),
    path(
        "eigen-nummer-is-toegevoegd/",
        views.AddCustomTrackSuccessView.as_view(),
        name="add-custom-track-success",
    ),
    path("api/search/", views.SpotipySearchView.as_view(), name="api-search"),
    path(
        "api/get/<str:spotifyuri>",
        views.SpotipyGetView.as_view(),
        name="api-get",
    ),
    path(
        "api/stats/", views.TrackStatsGetView.as_view(), name="api-track-stats"
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
    path(
        "dashboard/cms/hitlist/export/<str:pk>",
        views.HitListExportView.as_view(),
        name="hitlist-export",
    ),
    path(
        "dashboard/cms/similar-tracks",
        views.SimilarTrackView.as_view(),
        name="similar-track-list",
    ),
    path(
        "dashboard/cms/custom-track",
        views.CustomTrackListView.as_view(),
        name="custom-track-list",
    ),
    path(
        "dashboard/cms/custom-track/update/<str:pk>",
        views.CustomTrackUpdateView.as_view(),
        name="custom-track-update",
    ),
    path(
        "dashboard/cms/merge-tracks",
        views.MergeTracksView.as_view(),
        name="merge-tracks",
    ),
    path(
        "dashboard/cms/toggle-submission-invalidation/<str:votesubmissionid>",
        views.ToggleSubmissionInvalidation.as_view(),
        name="toggle-submission-invalidation",
    ),
    path(
        "dashboard/create-spotify-playlist/<str:hitlist_id>",
        views.HitListCreateSpotifyPlaylistView.as_view(),
        name="create-spotify-playlist",
    ),
    path(
        "dashboard/spotify-oauth",
        views.SpotifyOAuthView.as_view(),
        name="spotify-oauth",
    ),
]
