from rest_framework import serializers

from core.models.voting import HitList


class HitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HitList
        fields = ["name", "description"]
