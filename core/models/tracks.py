import uuid

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
        return artist_list(self.artists.all())

    def __str__(self):
        result = self.title + " - " + artist_list(self.artists.all())
        if self.is_non_spotify:
            result += " (Non Spotify)"
        return result
