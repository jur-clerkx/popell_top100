from django import forms

from core.models import VoteSubmission


class VoteSubmissionForm(forms.Form):
    name = forms.CharField(max_length=255, min_length=2, required=True)
    song_1 = forms.CharField(max_length=255, min_length=2, required=True)
    song_2 = forms.CharField(max_length=255, min_length=2, required=True)
    song_3 = forms.CharField(max_length=255, min_length=2, required=True)
    song_4 = forms.CharField(max_length=255, min_length=2, required=True)
    song_5 = forms.CharField(max_length=255, min_length=2, required=True)

    def clean(self):
        cleaned_data = super().clean()
        song_1 = cleaned_data.get("song_1")
        song_2 = cleaned_data.get("song_2")
        song_3 = cleaned_data.get("song_3")
        song_4 = cleaned_data.get("song_4")
        song_5 = cleaned_data.get("song_5")
        song_set = {song_1, song_2, song_3, song_4, song_5}
        if len(song_set) != 5:
            raise forms.ValidationError(
                "U kunt niet 2 of meerder keren op hetzelfde nummer stemmen."
            )
        return super().clean()

    def save(self):
        cleaned_data = super().clean()
        return VoteSubmission.create_vote_submission(
            cleaned_data.get("name"),
            cleaned_data.get("song_1"),
            cleaned_data.get("song_2"),
            cleaned_data.get("song_3"),
            cleaned_data.get("song_4"),
            cleaned_data.get("song_5"),
        )
