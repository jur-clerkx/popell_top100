from django.db import transaction

from core.models.settings import HitListSettings
from core.models.voting import HitList


class SettingsService:
    @staticmethod
    @transaction.atomic
    def get_current_hitlist() -> "HitList":
        return SettingsService.get_settings().current_hitlist

    @staticmethod
    @transaction.atomic
    def get_settings() -> "HitListSettings":
        current_settings = HitListSettings.objects.first()
        if current_settings is None:
            current_settings = HitListSettings()
            current_settings.current_hitlist = HitList.objects.first()
            current_settings.save()
        return current_settings

    @staticmethod
    @transaction.atomic
    def set_current_hitlist(hitlist: "HitList") -> None:
        if hitlist is not None:
            settings = SettingsService.get_settings()
            settings.current_hitlist = hitlist
            settings.save()
