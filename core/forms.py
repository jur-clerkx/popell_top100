from django import forms

from core.models.voting import VoteSubmission
from core.models.tracks import Track
from core.services.tracks import TrackService
from core.services.voting import VoteSubmissionService
from core.widgets import TrackSelectWidget


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
        return cleaned_data

    def save(self):
        cleaned_data = super().clean()
        return VoteSubmissionService.create_vote_submission(
            cleaned_data.get("name"),
            cleaned_data.get("song_1"),
            cleaned_data.get("song_2"),
            cleaned_data.get("song_3"),
            cleaned_data.get("song_4"),
            cleaned_data.get("song_5"),
        )


class CustomTrackForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=2, required=True)
    artist = forms.CharField(max_length=255, min_length=2, required=True)

    def save(self):
        cleaned_data = super().clean()
        return TrackService.create_custom_track(
            cleaned_data["title"], cleaned_data["artist"]
        )


class MergeTracksForm(forms.Form):
    merge_from = forms.ModelChoiceField(
        Track.objects.all().order_by("title").prefetch_related("artists"),
        required=True,
        widget=TrackSelectWidget(),
    )
    merge_to = forms.ModelChoiceField(
        Track.objects.all().order_by("title").prefetch_related("artists"),
        required=True,
        widget=TrackSelectWidget(),
    )

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["merge_from"] == cleaned_data["merge_to"]:
            raise forms.ValidationError(
                "Selecteer 2 verschillende nummers om samen te voegen!"
            )
        return cleaned_data

    def save(self):
        cleaned_data = super().clean()
        TrackService.merge_tracks(
            cleaned_data["merge_from"].id, cleaned_data["merge_to"].id
        )
