from django.test import TestCase

from core.models.tracks import Track


class TrackTests(TestCase):
    def test_create_track_with_incorrect_spotify_uri(self):
        with self.assertRaises(Exception):
            Track.get_or_create_song_by_uri("incorrect_uri")
        self.assertEqual(
            0, Track.objects.count(), "Track shouldn't be created!"
        )

    def test_create_track_correct_spotify_uri(self):
        Track.get_or_create_song_by_uri("spotify:track:4uUG5RXrOk84mYEfFvj3cK")
        self.assertEqual(
            1, Track.objects.count(), "Track should be saved to database!"
        )
        Track.get_or_create_song_by_uri("spotify:track:6hgoYQDUcPyCz7LcTUHKxa")
        self.assertEqual(
            2, Track.objects.count(), "Track should be saved to database!"
        )

    def test_track_is_only_created_once(self):
        Track.get_or_create_song_by_uri("spotify:track:4uUG5RXrOk84mYEfFvj3cK")
        self.assertEqual(
            1, Track.objects.count(), "Track should be saved to database!"
        )
        Track.get_or_create_song_by_uri("spotify:track:6hgoYQDUcPyCz7LcTUHKxa")
        self.assertEqual(
            2, Track.objects.count(), "Track should be saved to database!"
        )

        Track.get_or_create_song_by_uri("spotify:track:4uUG5RXrOk84mYEfFvj3cK")
        Track.get_or_create_song_by_uri("spotify:track:6hgoYQDUcPyCz7LcTUHKxa")
        self.assertEqual(
            2, Track.objects.count(), "Tracks shouldn't be duplicated"
        )
