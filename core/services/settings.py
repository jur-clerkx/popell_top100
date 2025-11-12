from typing import Optional
from django.db import transaction

from core.models.voting import HitList
from django.http import HttpRequest

COOKIE_VALUE = "dashboard_hitlist_id"


class SettingsService:
    @staticmethod
    @transaction.atomic
    def get_current_hitlist(request: HttpRequest) -> Optional[HitList]:
        hitlist_id = request.session.get(COOKIE_VALUE)
        if hitlist_id is None:
            hitlist = HitList.objects.first()
            SettingsService.set_current_hitlist(request, hitlist)
            return hitlist
        return HitList.objects.get(id=hitlist_id)

    @staticmethod
    @transaction.atomic
    def set_current_hitlist(
        request: HttpRequest, hitlist: Optional[HitList]
    ) -> None:
        if hitlist is not None:
            request.session[COOKIE_VALUE] = str(hitlist.id)
