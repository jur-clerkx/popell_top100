import unittest
from unittest.mock import Mock, patch, PropertyMock
from core.services.tracks import SimilarTrackService


class TestSimilarTrackService(unittest.TestCase):
    @patch("core.services.tracks.Track")
    def test_similar_tracks_returns_matches_above_threshold(
        self, mock_track_model
    ):
        """Test that similar track names with score > 70 are returned"""
        # Arrange
        mock_track1 = Mock()
        mock_track1.full_track_string = "The Beatles - Let It Be"

        mock_track2 = Mock()
        mock_track2.full_track_string = "The Beatles - Let It Be (Remaster)"

        mock_track_model.objects.all.return_value = [mock_track1, mock_track2]

        # Act
        results = SimilarTrackService.get_similar_tracks()

        # Assert
        self.assertGreater(len(results), 0)
        self.assertTrue(
            any(
                result[0] == "The Beatles - Let It Be"
                and result[1] == "The Beatles - Let It Be (Remaster)"
                and result[2] > 70
                for result in results
            )
        )

    @patch("core.services.tracks.Track")
    def test_dissimilar_tracks_not_returned(self, mock_track_model):
        """Test that dissimilar track names with score <= 70 are not returned"""
        # Arrange
        mock_track1 = Mock()
        mock_track1.full_track_string = "The Beatles - Let It Be"

        mock_track2 = Mock()
        mock_track2.full_track_string = "Pink Floyd - Comfortably Numb"

        mock_track_model.objects.all.return_value = [mock_track1, mock_track2]

        # Act
        results = SimilarTrackService.get_similar_tracks()

        # Assert
        self.assertFalse(
            any(
                (
                    result[0] == "The Beatles - Let It Be"
                    and result[1] == "Pink Floyd - Comfortably Numb"
                )
                or (
                    result[0] == "Pink Floyd - Comfortably Numb"
                    and result[1] == "The Beatles - Let It Be"
                )
                for result in results
            )
        )

    @patch("core.services.tracks.Track")
    def test_empty_track_list_returns_empty_results(self, mock_track_model):
        """Test that an empty track list returns empty results"""
        # Arrange
        mock_track_model.objects.all.return_value = []

        # Act
        results = SimilarTrackService.get_similar_tracks()

        # Assert
        self.assertEqual(results, [])

    @patch("core.services.tracks.Track")
    def test_single_track_returns_empty_results(self, mock_track_model):
        """Test that a single track returns empty results"""
        # Arrange
        mock_track = Mock()
        mock_track.full_track_string = "The Beatles - Let It Be"
        mock_track_model.objects.all.return_value = [mock_track]

        # Act
        results = SimilarTrackService.get_similar_tracks()

        # Assert
        self.assertEqual(results, [])
