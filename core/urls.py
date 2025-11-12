from django.urls import path


import core.views.dashboard as dashboard_views
import core.views.voting as voting_views


app_name = "core"
urlpatterns = [
    path("", voting_views.IndexView.as_view(), name="index"),
    path("closed/", voting_views.HitlistClosedView.as_view(), name="closed"),
    path("stemmen/", voting_views.VoteView.as_view(), name="vote"),
    path(
        "stem/<uuid:pk>",
        voting_views.VoteSubmissionDetailView.as_view(),
        name="vote-submission-detail",
    ),
    path(
        "eigen-nummer-toegevoegen/",
        voting_views.AddCustomTrackView.as_view(),
        name="add-custom-track",
    ),
    path(
        "eigen-nummer-is-toegevoegd/",
        voting_views.AddCustomTrackSuccessView.as_view(),
        name="add-custom-track-success",
    ),
    path(
        "dashboard/", dashboard_views.DashboardView.as_view(), name="dashboard"
    ),
    path(
        "dashboard/cms/hitlist",
        dashboard_views.HistListListView.as_view(),
        name="hitlist-list",
    ),
    path(
        "dashboard/cms/hitlist/create",
        dashboard_views.HitListCreateView.as_view(),
        name="hitlist-create",
    ),
    path(
        "dashboard/cms/hitlist/update/<str:pk>",
        dashboard_views.HitListUpdateView.as_view(),
        name="hitlist-update",
    ),
    path(
        "dashboard/cms/hitlist/delete/<str:pk>",
        dashboard_views.HitListDeleteView.as_view(),
        name="hitlist-delete",
    ),
    path(
        "dashboard/cms/hitlist/export/<str:pk>",
        dashboard_views.HitListExportView.as_view(),
        name="hitlist-export",
    ),
    path(
        "dashboard/cms/similar-tracks",
        dashboard_views.SimilarTrackView.as_view(),
        name="similar-track-list",
    ),
    path(
        "dashboard/cms/custom-track",
        dashboard_views.CustomTrackListView.as_view(),
        name="custom-track-list",
    ),
    path(
        "dashboard/cms/custom-track/update/<str:pk>",
        dashboard_views.CustomTrackUpdateView.as_view(),
        name="custom-track-update",
    ),
    path(
        "dashboard/cms/merge-tracks",
        dashboard_views.MergeTracksView.as_view(),
        name="merge-tracks",
    ),
    path(
        "dashboard/cms/toggle-submission-invalidation/<str:votesubmissionid>",
        dashboard_views.ToggleSubmissionInvalidation.as_view(),
        name="toggle-submission-invalidation",
    ),
    path(
        "dashboard/create-spotify-playlist/<str:hitlist_id>",
        dashboard_views.HitListCreateSpotifyPlaylistView.as_view(),
        name="create-spotify-playlist",
    ),
    path(
        "dashboard/spotify-oauth",
        dashboard_views.SpotifyOAuthView.as_view(),
        name="spotify-oauth",
    ),
]
