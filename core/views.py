import json
import os
import spotipy
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from spotipy.oauth2 import SpotifyClientCredentials
from django.views.generic import TemplateView
from django.utils.translation import activate

from core.forms import VoteSubmissionForm


class IndexView(TemplateView):
    template_name = "index.html"


class VoteView(View):
    template_name = "vote.html"

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {"voteForm": VoteSubmissionForm()}
        )

    def post(self, request, *args, **kwargs):
        activate("nl")  # Make sure errors are displayed in correct language
        form = VoteSubmissionForm(request.POST)
        form.is_valid()
        return render(request, self.template_name, {"voteForm": form})


spotipy_credentials = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
)


class SpotipySearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q")
        spotify = spotipy.Spotify(
            client_credentials_manager=spotipy_credentials
        )
        search_result = spotify.search(
            q=q, limit=10, type="track", market="NL"
        )
        found_tracks = search_result["tracks"]["items"]
        formatted_results = []
        for track in found_tracks:
            formatted_results.append(
                {
                    "id": track["uri"],
                    "track_name": track["name"],
                    "track_artist": ", ".join(
                        artist["name"] for artist in track["artists"]
                    ),
                    "image": track["album"]["images"][0]["url"],
                }
            )
        return JsonResponse({"results": formatted_results})


class SpotipyGetView(View):
    def get(self, request, spotifyuri, *args, **kwargs):
        spotify = spotipy.Spotify(
            client_credentials_manager=spotipy_credentials
        )
        track = spotify.track(spotifyuri)
        formatted_result = {
            "id": track["uri"],
            "track_name": track["name"],
            "track_artist": ", ".join(
                artist["name"] for artist in track["artists"]
            ),
            "image": track["album"]["images"][0]["url"],
        }
        return JsonResponse(formatted_result)
