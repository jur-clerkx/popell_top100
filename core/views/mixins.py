from django.shortcuts import redirect
from django.views import View

from core.services.voting import HitListService


class OpenHitListRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if (
            not HitListService.get_current_hitlist()
            or HitListService.get_current_hitlist().is_closed
        ):
            return redirect("core:closed")
        return super().dispatch(request, *args, **kwargs)
