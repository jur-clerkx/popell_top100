from rest_framework import generics

from core.models.voting import HitList
from core.rest_api.serializers import HitListSerializer
from core.services.settings import SettingsService


class CurrentHitListView(generics.RetrieveAPIView):
    serializer_class = HitListSerializer

    def get_object(self):
        return SettingsService.get_current_hitlist()

    def get_queryset(self):
        return HitList.objects.all()
