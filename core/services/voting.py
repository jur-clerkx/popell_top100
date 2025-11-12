import datetime

import django_excel  # type: ignore
from django.db import transaction

from core.exceptions import NoOpenHitListException
from core.models.voting import HitList, VoteSubmission, Vote
from core.services.tracks import TrackService
from core.spotify import spotify


class HitListService:
    @staticmethod
    def get_by_year(year: int) -> HitList:
        hitlist = HitList.objects.filter(vote_start_date__year=year).first()
        if hitlist is None:
            raise NoOpenHitListException(f"No hitlist found for year {year}")
        return hitlist

    @staticmethod
    def create_spotify_list(hitlist: HitList, access_token: str):
        spotify.create_playlist(hitlist.name, hitlist.get_list(), access_token)

    @staticmethod
    def get_current_hitlist():
        return (
            HitList.objects.filter(
                vote_start_date__lte=datetime.datetime.now(),
                vote_end_date__gte=datetime.datetime.now(),
            )
            .prefetch_related("votesubmission_set__vote_set__track__artists")
            .first()
        )

    @staticmethod
    def export_to_excel(hitlist: HitList):
        return django_excel.make_response_from_query_sets(
            hitlist.get_list(),
            ["title", "artist_string", "score", "votes"],
            "xlsx",
            file_name=hitlist.name + ".xlsx",
        )


class VoteSubmissionService:
    @staticmethod
    @transaction.atomic
    def create_vote_submission(
        name, song_1_uri, song_2_uri, song_3_uri, song_4_uri, song_5_uri
    ):
        hitlist = HitListService.get_current_hitlist()
        if not hitlist:
            raise NoOpenHitListException(
                "Er is geen open hitlijst op dit moment!"
            )
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
