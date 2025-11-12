from django.test import TestCase

from core.models.music import Track
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
