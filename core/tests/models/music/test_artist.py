from django.test import SimpleTestCase

from core.models.music import Artist


class ArtistModelTest(SimpleTestCase):
    def test_should_return_name_as_string_representation(self):
        artist = Artist(name="Test Artist")
        self.assertEqual(str(artist), "Test Artist")
