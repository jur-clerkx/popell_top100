import os

from spotipy import Spotify, SpotifyClientCredentials, SpotifyOAuth

from core.spotify.domain import Track, Artist
from core import models


def get_client():
    spotipy_credentials = SpotifyClientCredentials(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    )
    return Spotify(client_credentials_manager=spotipy_credentials)


def get_user_client():
    return Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private"))


def search_tracks(q):
    spotify = get_client()
    search_result = spotify.search(q=q, limit=10, type="track", market="NL")
    found_tracks = search_result["tracks"]["items"]
    formatted_tracks = []
    for track in found_tracks:
        formatted_tracks.append(Track.from_json(track))
    return formatted_tracks


def search_custom_tracks(q):
    found_tracks = models.Track.objects.filter(
        title__icontains=q, is_non_spotify=True
    ) | models.Track.objects.filter(
        artists__name__icontains=q, is_non_spotify=True
    )
    formatted_tracks = []
    for track in found_tracks:
        formatted_tracks.append(Track.from_model(track))
    return formatted_tracks


def get_track_by_uri(uri):
    if uri.startswith("spotify:track:"):
        return get_track_by_spotify_uri(uri)
    else:
        return Track.from_model(models.Track.objects.get(id=uri))


def get_track_by_spotify_uri(uri):
    spotify = get_client()
    track = spotify.track(uri)
    return Track.from_json(track)


def get_artist_by_uri(uri):
    spotify = get_client()
    artist = spotify.artist(uri)
    return Artist.from_json(artist)


def create_playlist(name, tracks):
    spotify = get_user_client()
    user_id = spotify.current_user()["id"]
    playlist_id = spotify.user_playlist_create(user_id, name, public=False)[
        "id"
    ]
    track_ids = []
    for track in tracks:
        if not track.is_non_spotify:
            track_ids.append(track.spotify_uri)
    spotify.playlist_add_items(playlist_id, track_ids)
