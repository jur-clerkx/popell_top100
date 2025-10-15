from django.db import models, transaction

from core.models.tracks import Artist, Track
from core.models.voting import Vote
from core.spotify import spotify


class ArtistService:
    @staticmethod
    def get_or_create_artist_by_uri(artist_uri):
        try:
            return Artist.objects.get(spotify_uri=artist_uri)
        except models.ObjectDoesNotExist:  # Create artist in the database
            # Check for similar name
            artist_json = spotify.get_artist_by_uri(artist_uri)
            same_artist = Artist.objects.filter(name=artist_json.name).first()
            if same_artist:
                return same_artist
            artist = Artist(
                name=artist_json.name,
                spotify_uri=artist_json.id,
                spotify_url=artist_json.spotify_url,
                is_non_spotify=False,
            )
            artist.save()
            return artist

    @staticmethod
    def create_custom_artist(name):
        existing = Artist.objects.filter(name=name).first()
        if existing:
            return existing
        artist = Artist(name=name, is_non_spotify=True)
        artist.save()
        return artist


class TrackService:
    @staticmethod
    def get_or_create_song_by_uri(song_uri):
        if song_uri.startswith("spotify:track:"):
            return TrackService.get_or_create_song_by_spotify_uri(song_uri)
        else:
            return Track.objects.get(id=song_uri)

    @staticmethod
    def get_or_create_song_by_spotify_uri(song_uri):
        try:
            return Track.objects.get(spotify_uri=song_uri)
        except models.ObjectDoesNotExist:  # Create track in the database
            track_json = spotify.get_track_by_uri(song_uri)
            artists = []
            for artist_json in track_json.track_artists:
                artists.append(
                    ArtistService.get_or_create_artist_by_uri(artist_json.id)
                )
            track = Track(
                title=track_json.track_name,
                spotify_uri=track_json.id,
                spotify_url=track_json.spotify_url,
                preview_url=track_json.preview_url,
                image_url=track_json.image,
                is_non_spotify=False,
            )
            track.save()
            for artist in artists:
                track.artists.add(artist)
            return track

    @staticmethod
    @transaction.atomic
    def create_custom_track(track_title, track_artist):
        artist = ArtistService.create_custom_artist(track_artist)
        track = Track(title=track_title, is_non_spotify=True)
        track.save()
        track.artists.add(artist)
        return track

    @staticmethod
    @transaction.atomic
    def merge_tracks(from_id, to_id):
        """Merges all the votes from the from track to the to track and deletes the from track."""
        from_track = Track.objects.get(id=from_id)
        to_track = Track.objects.get(id=to_id)
        votes = Vote.objects.filter(track=from_track)
        for vote in votes:
            vote.track = to_track
            vote.save()
        from_track.delete()
