from django.test import TestCase
from core.models import tracks as models
from core.spotify.domain import Track, Artist


class TrackTests(TestCase):
    def test_should_parse_copy_id(self):
        track = models.Track(id=1)
        result = Track.from_model(track)
        self.assertEqual(result.id, 1)

    def test_should_parse_copy_title(self):
        track = models.Track(title="test")
        result = Track.from_model(track)
        self.assertEqual(result.track_name, "test")

    def test_should_parse_copy_artists(self):
        track = models.Track(title="test")
        track.save()
        artist1 = models.Artist(name="artist 1")
        artist1.save()
        artist2 = models.Artist(name="artist 2")
        artist2.save()
        track.artists.add(artist1, artist2)

        expected = [
            Artist(artist1.id, artist1.name, ""),
            Artist(artist2.id, artist2.name, ""),
        ]
        expected.sort(key=lambda x: x.id)
        result = Track.from_model(track)
        self.assertListEqual(result.track_artists, expected)

    def test_should_parse_should_copy_image_if_set(self):
        track = models.Track()
        result = Track.from_model(track)
        self.assertEqual(result.image, "")
        track.image_url = "testurl"
        result = Track.from_model(track)
        self.assertEqual(result.image, "testurl")

    def test_should_parse_should_copy_preview_if_set(self):
        track = models.Track()
        result = Track.from_model(track)
        self.assertEqual(result.preview_url, "")
        track.preview_url = "testurl"
        result = Track.from_model(track)
        self.assertEqual(result.preview_url, "testurl")
