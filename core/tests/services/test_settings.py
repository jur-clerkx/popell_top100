from datetime import datetime, timedelta
from django.test import TestCase

from core.models.voting import HitList
from core.services.settings import COOKIE_VALUE, SettingsService


class SettingsServiceTests(TestCase):
    def _create_hitlist(self, name: str):
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)
        hitlist = HitList.objects.create(
            name=name,
            vote_start_date=yesterday,
            vote_end_date=tomorrow,
        )
        return hitlist

    def test_set_current_hitlist_stores_in_session(self):
        hl = self._create_hitlist("Test HitList")
        request = self._create_request()
        SettingsService.set_current_hitlist(request, hl)
        self.assertEqual(request.session[COOKIE_VALUE], hl.id)

    def test_set_current_hitlist_with_none_does_nothing(self):
        request = self._create_request()
        request.session[COOKIE_VALUE] = 999
        SettingsService.set_current_hitlist(request, None)
        self.assertEqual(request.session[COOKIE_VALUE], 999)

    def test_get_current_hitlist_returns_from_session(self):
        hl = self._create_hitlist("Test HitList")
        request = self._create_request()
        request.session[COOKIE_VALUE] = hl.id
        current = SettingsService.get_current_hitlist(request)
        self.assertEqual(current.pk, hl.pk)

    def test_get_current_hitlist_fallback_to_first_when_missing(self):
        hl = self._create_hitlist("First HitList")
        request = self._create_request()
        # session key not set or None
        current = SettingsService.get_current_hitlist(request)
        self.assertEqual(current.pk, hl.pk)
        self.assertEqual(request.session[COOKIE_VALUE], hl.id)

    def _create_request(self):
        from django.test import RequestFactory

        factory = RequestFactory()
        req = factory.get("/")
        req.session = {}
        return req
