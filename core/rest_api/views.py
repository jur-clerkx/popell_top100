from rest_framework import generics
from dataclasses import asdict

from core.models.music import Track
from core.models.voting import HitList, Vote, VoteSubmission
from core.rest_api.serializers import HitListSerializer
from core.services.settings import SettingsService
from rest_framework.views import APIView
from rest_framework.response import Response

from core.services.voting import HitListService
from core.spotify import spotify
from rest_framework import status
from rest_framework import permissions


class CurrentHitListView(generics.RetrieveAPIView):
    serializer_class = HitListSerializer

    def get_object(self):
        return SettingsService.get_current_hitlist()

    def get_queryset(self):
        return HitList.objects.all()


class SpotipySearchView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        q = request.GET.get("q")
        search_results = spotify.search_custom_tracks(
            q
        ) + spotify.search_tracks(q)
        return Response({"results": [asdict(x) for x in search_results]})


class SpotipyGetView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, spotifyuri, format=None):
        return Response(asdict(spotify.get_track_by_uri(spotifyuri)))


class TrackStatsGetView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        title = request.GET.get("title", "")
        year = request.GET.get("year", "")
        artist = request.GET.get("artist", "")
        track_uri = request.GET.get("spotify_uri", "")
        print(title, year, artist, track_uri)
        hitlist = HitListService.get_by_year(year)
        track = Track.find_by_uri_or_title(track_uri, title)
        if track is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Track not found!"},
            )
        votes = Vote.objects.filter(
            track=track,
            submission__hit_list=hitlist,
            submission__is_invalidated=False,
        )
        if votes.count() == 0:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"error": "Track not part of hitlist!"},
            )
        position = 1
        for entry in hitlist.get_list():
            if entry.id == track.id:
                break
            position += 1
        vote_count, points = 0, 0
        for vote in votes:
            vote_count += 1
            points += vote.points
        votes = VoteSubmission.objects.filter(
            hit_list=hitlist, vote__track=track, is_invalidated=False
        ).values("submitter_name")
        return Response(
            {
                "track": str(track),
                "position": position,
                "points": points,
                "number_of_votes": vote_count,
                "voters": list(votes),
            }
        )
