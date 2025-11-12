# python
from unittest.mock import patch
import datetime

from django.test import TestCase

from core.exceptions import NoOpenHitListException
from core.models.voting import HitList
from core.services.voting import HitListService


class HitListServiceTests(TestCase):
    def test_get_by_year_returns_hitlist(self):
        year = datetime.datetime.now().year
        hitlist = HitList.objects.create(
            name="TestListByYear",
            vote_start_date=datetime.datetime(year, 1, 1, 0, 0, 0),
            vote_end_date=datetime.datetime(year, 12, 31, 23, 59, 59),
            description="desc",
        )
        found = HitListService.get_by_year(year)
        self.assertIsNotNone(found)
        self.assertEqual(found.id, hitlist.id)

    def test_get_by_year_raises_when_not_found(self):
        year = 3000  # future year unlikely to have data
        with self.assertRaises(NoOpenHitListException):
            HitListService.get_by_year(year)

    def test_get_current_hitlist_returns_when_open(self):
        now = datetime.datetime.now()
        hitlist = HitList.objects.create(
            name="CurrentList",
            vote_start_date=now - datetime.timedelta(days=1),
            vote_end_date=now + datetime.timedelta(days=1),
            description="desc",
        )
        current = HitListService.get_current_hitlist()
        self.assertIsNotNone(current)
        self.assertEqual(current.id, hitlist.id)

    def test_get_current_hitlist_returns_none_when_closed(self):
        # Create a hitlist entirely in the past
        now = datetime.datetime.now()
        HitList.objects.create(
            name="PastList",
            vote_start_date=now - datetime.timedelta(days=10),
            vote_end_date=now - datetime.timedelta(days=5),
            description="desc",
        )
        current = HitListService.get_current_hitlist()
        self.assertIsNone(current)

    def test_create_spotify_list_calls_spotify_create_playlist(self):
        # Create a hitlist instance
        hitlist = HitList.objects.create(
            name="SpotifyExportList",
            vote_start_date=datetime.datetime.now()
            - datetime.timedelta(days=1),
            vote_end_date=datetime.datetime.now() + datetime.timedelta(days=1),
            description="desc",
        )
        sentinel_list = ["track_a", "track_b"]
        access_token = "token123"

        # Patch HitList.get_list to return our sentinel list and patch the spotify module imported in the service
        with patch.object(HitList, "get_list", return_value=sentinel_list):
            with patch("core.services.voting.spotify") as mock_spotify:
                HitListService.create_spotify_list(hitlist, access_token)
                mock_spotify.create_playlist.assert_called_once_with(
                    hitlist.name, sentinel_list, access_token
                )
