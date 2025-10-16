from django.urls import path, include
from rest_framework import routers

from core.rest_api.views import CurrentHitListView

router = routers.SimpleRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("current_hitlist/", CurrentHitListView.as_view()),
]
