from django.test import TestCase

from core.models.music import Artist, Track


class TrackModelTest(TestCase):
    def setUp(self):
        self.a1 = Artist.objects.create(name="Artist One")
        self.a2 = Artist.objects.create(name="Artist Two")

    def test_should_return_artist_and_title_in_full_track_string(self):
        track = Track.objects.create(title="My Song")
        track.artists.add(self.a1, self.a2)

        self.assertEqual(
            track.full_track_string, "My Song - Artist Two, Artist One"
        )

    def test_should_return_full_track_string_without_non_spotify_marker_as_string_representation_for_spotify_track(
        self,
    ):
        track = Track.objects.create(title="My Song")
        track.artists.add(self.a1, self.a2)

        self.assertEqual(str(track), "My Song - Artist One, Artist Two")

    def test_should_return_full_track_string_with_non_spotify_marker_as_string_representation_for_non_spotify_track(
        self,
    ):
        track = Track.objects.create(title="My Song", is_non_spotify=True)
        track.artists.add(self.a1, self.a2)
        self.assertEqual(
            str(track), "My Song - Artist Two, Artist One (Non Spotify)"
        )

    def test_should_return_non_if_no_uri_or_title_provided(self):
        result = Track.find_by_uri_or_title(None, None)
        self.assertIsNone(result)

    def test_should_return_track_by_spotify_uri_first(self):
        t_uri = Track.objects.create(
            title="URI Song", spotify_uri="spotify:track:123"
        )
        Track.objects.create(title="URI Song duplicate")

        found_by_uri = Track.find_by_uri_or_title(
            "spotify:track:123", "URI Song duplicate"
        )
        self.assertIsNotNone(found_by_uri)
        self.assertEqual(found_by_uri.id, t_uri.id)

    def test_should_return_track_by_title_if_no_uri_match(self):
        t_title = Track.objects.create(title="Only Title Song")

        found_by_title = Track.find_by_uri_or_title(
            "spotify:track:nonexistent", "Only Title Song"
        )
        self.assertIsNotNone(found_by_title)
        self.assertEqual(found_by_title.id, t_title.id)
