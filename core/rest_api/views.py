from rest_framework import generics

from core.models import HitList
from core.rest_api.serializers import HitListSerializer


class CurrentHitListView(generics.RetrieveAPIView):
    serializer_class = HitListSerializer

    def get_object(self):
        return HitList.get_current_hitlist()

    def get_queryset(self):
        return HitList.objects.all()
