from django.test import TestCase
from datetime import datetime, timedelta

from core.models.voting import VoteSubmission, HitList, Vote
from core.models.tracks import Track
from core.services.voting import VoteSubmissionService


def setup_hitlist():
    yesterday = datetime.now() - timedelta(days=1)
    tomorrow = datetime.now() + timedelta(days=1)
    HitList.objects.create(
        name="Testlist",
        vote_start_date=yesterday,
        vote_end_date=tomorrow,
    )


class VoteSubmissionTests(TestCase):
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

    def test_create_vote_submissions_partial_incorrect_tracks(self):
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

    def test_create_vote_submission_correct(self):
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
