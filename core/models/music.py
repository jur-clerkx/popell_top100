import uuid
from typing import Optional

from django.db import models

from core.templatetags.core_extras import artist_list


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, blank=False, null=False, unique=True
    )

    # Spotify data
    spotify_uri = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    spotify_url = models.CharField(max_length=255, blank=True, null=True)

    # Boolean field to check if artist is from spotify
    is_non_spotify = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Track(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    artists = models.ManyToManyField(Artist)

    # Spotify data
    spotify_uri = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    preview_url = models.CharField(max_length=255, blank=True, null=True)
    spotify_url = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)

    # Boolean field to check if track is from spotify
    is_non_spotify = models.BooleanField(default=False)

    @property
    def artist_string(self) -> str:
        return artist_list(self.artists.all().order_by("name"))

    @staticmethod
    def find_by_uri_or_title(
        spotify_uri: Optional[str], title: Optional[str]
    ) -> Optional["Track"]:
        track = None
        if spotify_uri:
            track = Track.objects.filter(spotify_uri=spotify_uri).first()
        if title and track is None:
            return Track.objects.filter(title=title).first()
        return track

    @property
    def full_track_string(self):
        return self.title + " - " + self.artist_string

    def __str__(self):
        result = self.title + " - " + self.artist_string
        if self.is_non_spotify:
            result += " (Non Spotify)"
        return result
