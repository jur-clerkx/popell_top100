from django.test import TestCase

from core.models.tracks import Artist


class ArtistTests(TestCase):
    def test_create_artist_with_incorrect_spotify_uri(self):
        with self.assertRaises(Exception):
            Artist.get_or_create_artist_by_uri("incorrect_uri")
        self.assertEqual(
            0, Artist.objects.count(), "Track shouldn't be created!"
        )

    def test_create_artist_correct_spotify_uri(self):
        Artist.get_or_create_artist_by_uri(
            "spotify:artist:5ENS85nZShljwNgg4wFD7D"
        )
        self.assertEqual(
            1, Artist.objects.count(), "Track should be saved to database!"
        )
        Artist.get_or_create_artist_by_uri(
            "spotify:artist:0xRXCcSX89eobfrshSVdyu"
        )
        self.assertEqual(
            2, Artist.objects.count(), "Track should be saved to database!"
        )

    def test_artist_is_only_created_once(self):
        Artist.get_or_create_artist_by_uri(
            "spotify:artist:5ENS85nZShljwNgg4wFD7D"
        )
        self.assertEqual(
            1, Artist.objects.count(), "Track should be saved to database!"
        )
        Artist.get_or_create_artist_by_uri(
            "spotify:artist:0xRXCcSX89eobfrshSVdyu"
        )
        self.assertEqual(
            2, Artist.objects.count(), "Track should be saved to database!"
        )

        Artist.get_or_create_artist_by_uri(
            "spotify:artist:5ENS85nZShljwNgg4wFD7D"
        )
        Artist.get_or_create_artist_by_uri(
            "spotify:artist:0xRXCcSX89eobfrshSVdyu"
        )
        self.assertEqual(
            2, Artist.objects.count(), "Tracks shouldn't be duplicated"
        )
