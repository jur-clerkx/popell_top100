from datetime import datetime, timedelta
from django.test import TestCase

from core.models.settings import HitListSettings
from core.models.voting import HitList
from core.services.settings import SettingsService


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

    def test_get_settings_creates_default_with_existing_hitlist(self):
        # Ensure there is a HitList in DB
        hl = self._create_hitlist("Test HitList")
        # Make sure no settings exist
        HitListSettings.objects.all().delete()

        settings = SettingsService.get_settings()
        self.assertIsNotNone(settings)
        # current_hitlist should be set to the first HitList (the one we created)
        self.assertIsNotNone(settings.current_hitlist)
        self.assertEqual(settings.current_hitlist.pk, hl.pk)

    def test_get_current_hitlist_returns_assigned(self):
        hl = self._create_hitlist("Test HitList")
        # Create settings explicitly pointing to our hitlist
        hs = HitListSettings.objects.create(current_hitlist=hl)
        current = SettingsService.get_current_hitlist()
        self.assertEqual(current.pk, hs.current_hitlist.pk)
        self.assertEqual(current.pk, hl.pk)

    def test_set_current_hitlist_updates(self):
        first = self._create_hitlist("First HitList")
        second = self._create_hitlist("Second HitList")
        # Ensure settings exist and point to first
        hs = HitListSettings.objects.create(current_hitlist=first)
        SettingsService.set_current_hitlist(second)

        hs.refresh_from_db()
        self.assertEqual(hs.current_hitlist.pk, second.pk)

    def test_set_current_hitlist_with_none_does_nothing(self):
        hl = self._create_hitlist("Test HitList")
        hs = HitListSettings.objects.create(current_hitlist=hl)
        SettingsService.set_current_hitlist(None)
        hs.refresh_from_db()
        # should remain unchanged
        self.assertEqual(hs.current_hitlist.pk, hl.pk)
