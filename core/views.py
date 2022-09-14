import json
import os
import spotipy
from django.http import JsonResponse
from spotipy.oauth2 import SpotifyClientCredentials

from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class VoteView(TemplateView):
    template_name = "vote.html"


spotipy_credentials = SpotifyClientCredentials(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
)


def spotipy_search(request):
    q = request.GET.get("q")
    spotify = spotipy.Spotify(client_credentials_manager=spotipy_credentials)
    search_result = spotify.search(q=q, limit=5, type="track", market="NL")
    found_tracks = search_result["tracks"]["items"]
    formatted_results = []
    for track in found_tracks:
        formatted_results.append(
            {
                "id": track["uri"],
                "text": track["name"] + " - " + track["artists"][0]["name"],
                "image": track["album"]["images"][0]["url"],
            }
        )
    return JsonResponse({"results": formatted_results})
