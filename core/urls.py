from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("stemmen/", views.VoteView.as_view(), name="stemmen"),
    path("api/search/", views.SpotipySearchView.as_view(), name="api-search"),
]