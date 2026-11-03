from unittest.mock import MagicMock, patch
from django.test import TestCase

from core.models.music import Artist
from core.services.music import ArtistService


def _mock_artist(uri: str):
    artist = MagicMock()
    artist.id = uri
    artist.name = f"Artist {uri}"
    artist.spotify_url = f"https://open.spotify.com/artist/{uri}"
    return artist


class ArtistServiceTests(TestCase):
    @patch(
        "core.spotify.spotify.get_artist_by_uri",
        side_effect=Exception("Invalid URI"),
    )
    def test_create_artist_with_incorrect_spotify_uri(
        self, _mock_get_artist_by_uri
    ):
        with self.assertRaises(Exception):
            ArtistService.get_or_create_artist_by_uri("incorrect_uri")
        self.assertEqual(
            0, Artist.objects.count(), "Track shouldn't be created!"
        )

    @patch("core.spotify.spotify.get_artist_by_uri", side_effect=_mock_artist)
    def test_create_artist_correct_spotify_uri(self, _mock_get_artist_by_uri):
        ArtistService.get_or_create_artist_by_uri(
            "spotify:artist:5ENS85nZShljwNgg4wFD7D"
        )
        self.assertEqual(
            1, Artist.objects.count(), "Track should be saved to database!"
        )
        ArtistService.get_or_create_artist_by_uri(
            "spotify:artist:0xRXCcSX89eobfrshSVdyu"
        )
        self.assertEqual(
            2, Artist.objects.count(), "Track should be saved to database!"
        )

    @patch("core.spotify.spotify.get_artist_by_uri", side_effect=_mock_artist)
    def test_artist_is_only_created_once(self, _mock_get_artist_by_uri):
        ArtistService.get_or_create_artist_by_uri(
            "spotify:artist:5ENS85nZShljwNgg4wFD7D"
        )
        self.assertEqual(
            1, Artist.objects.count(), "Track should be saved to database!"
        )
        ArtistService.get_or_create_artist_by_uri(
            "spotify:artist:0xRXCcSX89eobfrshSVdyu"
        )
        self.assertEqual(
            2, Artist.objects.count(), "Track should be saved to database!"
        )

        ArtistService.get_or_create_artist_by_uri(
            "spotify:artist:5ENS85nZShljwNgg4wFD7D"
        )
        ArtistService.get_or_create_artist_by_uri(
            "spotify:artist:0xRXCcSX89eobfrshSVdyu"
        )
        self.assertEqual(
            2, Artist.objects.count(), "Tracks shouldn't be duplicated"
        )
