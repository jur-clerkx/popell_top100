from django.test import TestCase
from core.models import tracks as models

from core.spotify import spotify


class SearchCustomTracksTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        artist1 = models.Artist(name="TEST ARTIST", is_non_spotify=True)
        artist1.save()
        artist2 = models.Artist(name="number two", is_non_spotify=True)
        artist2.save()
        track1 = models.Track(title="Track 1", is_non_spotify=True)
        track1.save()
        track1.artists.add(artist1)
        track2 = models.Track(title="Track 2", is_non_spotify=True)
        track2.save()
        track2.artists.add(artist2)

    def test_should_search_artist_name_case_insensitive(self) -> None:
        self.assertEqual(len(spotify.search_custom_tracks("test artist")), 1)
        self.assertEqual(len(spotify.search_custom_tracks("NUMBER TWO")), 1)
        self.assertEqual(len(spotify.search_custom_tracks("no artist")), 0)
        self.assertEqual(len(spotify.search_custom_tracks("TES")), 1)
        self.assertEqual(len(spotify.search_custom_tracks("NumbE")), 1)

    def test_should_search_track_title_case_insensitive(self) -> None:
        self.assertEqual(len(spotify.search_custom_tracks("TRACK")), 2)
        self.assertEqual(len(spotify.search_custom_tracks("1")), 1)
        self.assertEqual(len(spotify.search_custom_tracks("AcK")), 2)
        self.assertEqual(len(spotify.search_custom_tracks("TRACKS")), 0)
