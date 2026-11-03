from unittest.mock import MagicMock, patch
from django.test import TestCase
from datetime import datetime, timedelta

from core.models.voting import VoteSubmission, HitList, Vote
from core.models.music import Track
from core.services.voting import VoteSubmissionService


def setup_hitlist():
    yesterday = datetime.now() - timedelta(days=1)
    tomorrow = datetime.now() + timedelta(days=1)
    HitList.objects.create(
        name="Testlist",
        vote_start_date=yesterday,
        vote_end_date=tomorrow,
    )


def _mock_artist(uri: str):
    artist = MagicMock()
    artist.id = uri
    artist.name = f"Artist {uri}"
    artist.spotify_url = f"https://open.spotify.com/artist/{uri}"
    return artist


def _mock_track(uri: str):
    track = MagicMock()
    track.id = uri
    track.track_name = f"Track {uri}"
    track.spotify_url = f"https://open.spotify.com/track/{uri}"
    track.preview_url = f"https://p.scdn.co/mp3-preview/{uri}"
    track.image = f"https://i.scdn.co/image/{uri}"
    track.track_artists = [_mock_artist(f"spotify:artist:{uri}")]
    return track


class VoteSubmissionServiceTests(TestCase):
    def test_create_vote_submission_without_hitlist(self):
        with self.assertRaises(Exception):
            VoteSubmissionService.create_vote_submission(
                "jur", "track1", "track2", "track3", "track4", "track5"
            )

    def test_create_vote_submissions_incorrect_tracks(self):
        setup_hitlist()
        with self.assertRaises(Exception):
            VoteSubmissionService.create_vote_submission(
                "jur", "track1", "track2", "track3", "track4", "track5"
            )
        self.assertEqual(
            0, Track.objects.count(), "Tracks shouldn't been created!"
        )
        self.assertEqual(0, VoteSubmission.objects.count())

    @patch("core.spotify.spotify.get_artist_by_uri", side_effect=_mock_artist)
    @patch("core.spotify.spotify.get_track_by_uri", side_effect=_mock_track)
    def test_create_vote_submissions_partial_incorrect_tracks(
        self, _mock_get_track_by_uri, _mock_get_artist_by_uri
    ):
        setup_hitlist()
        with self.assertRaises(Exception):
            VoteSubmissionService.create_vote_submission(
                "jur",
                "spotify:track:4uUG5RXrOk84mYEfFvj3cK",
                "spotify:track:6hgoYQDUcPyCz7LcTUHKxa",
                "track3",
                "track4",
                "spotify:track:1bgKMxPQU7JIZEhNsM1vFs",
            )
        self.assertEqual(
            0, Track.objects.count(), "Tracks shouldn't been created!"
        )
        self.assertEqual(
            0,
            VoteSubmission.objects.count(),
            "Submissions shouldn't be created",
        )
        self.assertEqual(0, Vote.objects.count(), "Votes shouldn't be created")

    @patch("core.spotify.spotify.get_artist_by_uri", side_effect=_mock_artist)
    @patch("core.spotify.spotify.get_track_by_uri", side_effect=_mock_track)
    def test_create_vote_submission_correct(
        self, _mock_get_track_by_uri, _mock_get_artist_by_uri
    ):
        setup_hitlist()
        VoteSubmissionService.create_vote_submission(
            "jur",
            "spotify:track:4uUG5RXrOk84mYEfFvj3cK",
            "spotify:track:6hgoYQDUcPyCz7LcTUHKxa",
            "spotify:track:7j2TJXhcE1aAzB6Evmgvm0",
            "spotify:track:4LRPiXqCikLlN15c3yImP7",
            "spotify:track:1bgKMxPQU7JIZEhNsM1vFs",
        )
        self.assertEqual(5, Track.objects.count(), "Tracks aren't created!")
        self.assertEqual(
            1, VoteSubmission.objects.count(), "Submission isn't created!"
        )
        self.assertEqual(5, Vote.objects.count(), "Votes aren't created!")
