from django.test import TestCase

from core.forms import VoteSubmissionForm


class VoteSubmissionFormTests(TestCase):
    test_data = {
        "name": "Test User",
        "song_1": "spotify:track:4uUG5RXrOk84mYEfFvj3cK",
        "song_2": "spotify:track:6hgoYQDUcPyCz7LcTUHKxa",
        "song_3": "spotify:track:0QPRDC97rIQB3Jh3hrVJoH",
        "song_4": "spotify:track:1bgKMxPQU7JIZEhNsM1vFs",
        "song_5": "spotify:track:3rb0tMq42WfggucPm0HHkA",
    }

    def test_duplicate_song_entries(self):
        data = self.test_data.copy()
        data["song_1"] = data["song_2"]
        form = VoteSubmissionForm(data=data)
        self.assertEqual(1, len(form.non_field_errors()))
        self.assertEqual(
            "U kunt niet 2 of meerder keren op hetzelfde nummer stemmen.",
            form.non_field_errors()[0],
        )

        data = self.test_data.copy()
        data["song_2"] = data["song_3"]
        form = VoteSubmissionForm(data=data)
        self.assertEqual(1, len(form.non_field_errors()))
        self.assertEqual(
            "U kunt niet 2 of meerder keren op hetzelfde nummer stemmen.",
            form.non_field_errors()[0],
        )

        data = self.test_data.copy()
        data["song_3"] = data["song_4"]
        form = VoteSubmissionForm(data=data)
        self.assertEqual(1, len(form.non_field_errors()))
        self.assertEqual(
            "U kunt niet 2 of meerder keren op hetzelfde nummer stemmen.",
            form.non_field_errors()[0],
        )

        data = self.test_data.copy()
        data["song_4"] = data["song_5"]
        form = VoteSubmissionForm(data=data)
        self.assertEqual(1, len(form.non_field_errors()))
        self.assertEqual(
            "U kunt niet 2 of meerder keren op hetzelfde nummer stemmen.",
            form.non_field_errors()[0],
        )
