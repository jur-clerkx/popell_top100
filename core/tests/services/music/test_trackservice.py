from unittest.mock import MagicMock, patch
from django.test import TestCase

from core.models.music import Artist, Track
from core.services.music import TrackService


class TrackServiceTests(TestCase):
    def test_create_track_with_incorrect_spotify_uri(self):
        with self.assertRaises(Exception):
            TrackService.get_or_create_song_by_uri("incorrect_uri")
        self.assertEqual(
            0, Track.objects.count(), "Track shouldn't be created!"
        )

    def test_create_track_correct_spotify_uri(self):
        TrackService.get_or_create_song_by_uri(
            "spotify:track:4uUG5RXrOk84mYEfFvj3cK"
        )
        self.assertEqual(
            1, Track.objects.count(), "Track should be saved to database!"
        )
        TrackService.get_or_create_song_by_uri(
            "spotify:track:6hgoYQDUcPyCz7LcTUHKxa"
        )
        self.assertEqual(
            2, Track.objects.count(), "Track should be saved to database!"
        )

    def test_track_is_only_created_once(self):
        TrackService.get_or_create_song_by_uri(
            "spotify:track:4uUG5RXrOk84mYEfFvj3cK"
        )
        self.assertEqual(
            1, Track.objects.count(), "Track should be saved to database!"
        )
        TrackService.get_or_create_song_by_uri(
            "spotify:track:6hgoYQDUcPyCz7LcTUHKxa"
        )
        self.assertEqual(
            2, Track.objects.count(), "Track should be saved to database!"
        )

        TrackService.get_or_create_song_by_uri(
            "spotify:track:4uUG5RXrOk84mYEfFvj3cK"
        )
        TrackService.get_or_create_song_by_uri(
            "spotify:track:6hgoYQDUcPyCz7LcTUHKxa"
        )
        self.assertEqual(
            2, Track.objects.count(), "Tracks shouldn't be duplicated"
        )

    @patch("core.spotify.spotify.get_track_by_uri")
    def test_song_with_different_spotify_uri_but_same_title_wont_duplicate(
        self, mock_get_track_by_uri
    ):
        # Create track with specific title and artists
        artist1 = Artist.objects.create(
            name="Artist 1",
            spotify_uri="spotify:artist:1",
            is_non_spotify=False,
        )
        artist2 = Artist.objects.create(
            name="Artist 2",
            spotify_uri="spotify:artist:2",
            is_non_spotify=False,
        )
        track = Track.objects.create(
            title="Track 1",
            spotify_uri="spotify:track:1",
            is_non_spotify=False,
        )
        track.artists.add(artist1)
        track.artists.add(artist2)
        track.save()

        # Mock the spotify response to return a track with the same title and artists but different URI
        mock_track = MagicMock()
        mock_track.id = "spotify:track:differenturi1234567890"
        mock_track.track_name = "Track 1"
        mock_track.spotify_url = (
            "https://open.spotify.com/track/differenturi1234567890"
        )
        mock_track.preview_url = "https://p.scdn.co/mp3-preview/differenturi"
        mock_track.image = "https://i.scdn.co/image/differenturi"
        mock_track.track_artists = [
            MagicMock(
                id="spotify:artist:1",
                name="Artist 1",
                spotify_url="https://open.spotify.com/artist/1",
            ),
            MagicMock(
                id="spotify:artist:2",
                name="Artist 2",
                spotify_url="https://open.spotify.com/artist/2",
            ),
        ]
        mock_get_track_by_uri.return_value = mock_track

        TrackService.get_or_create_song_by_uri(
            "spotify:track:differenturi1234567890"
        )
        self.assertEqual(
            1, Track.objects.count(), "Track should not be duplicated!"
        )
