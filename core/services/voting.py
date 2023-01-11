import datetime

from django.db import transaction

from core.models.voting import HitList, VoteSubmission, Vote
from core.services.tracks import TrackService
from core.spotify import spotify


class HitListService:
    @staticmethod
    def get_by_year(year: int) -> HitList:
        return HitList.objects.filter(vote_start_date__year=year).first()

    @staticmethod
    def create_spotify_list(hitlist: HitList, access_token: str):
        spotify.create_playlist(hitlist.name, hitlist.get_list(), access_token)


class VoteSubmissionService:
    @staticmethod
    @transaction.atomic
    def create_vote_submission(
        name, song_1_uri, song_2_uri, song_3_uri, song_4_uri, song_5_uri
    ):
        hitlist = HitListService.get_current_hitlist()
        if not hitlist:
            raise Exception("Er is geen open hitlijst op dit moment!")
        submission = VoteSubmission(submitter_name=name, hit_list=hitlist)
        submission.save()
        Vote.objects.create(
            track=TrackService.get_or_create_song_by_uri(song_1_uri),
            submission=submission,
            points=5,
        )
        Vote.objects.create(
            track=TrackService.get_or_create_song_by_uri(song_2_uri),
            submission=submission,
            points=4,
        )
        Vote.objects.create(
            track=TrackService.get_or_create_song_by_uri(song_3_uri),
            submission=submission,
            points=3,
        )
        Vote.objects.create(
            track=TrackService.get_or_create_song_by_uri(song_4_uri),
            submission=submission,
            points=2,
        )
        Vote.objects.create(
            track=TrackService.get_or_create_song_by_uri(song_5_uri),
            submission=submission,
            points=1,
        )
        return submission
