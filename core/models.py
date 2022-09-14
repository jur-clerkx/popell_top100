import uuid

from django.db import models


class HitList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, blank=False, null=False, unique=True
    )
    vote_start_date = models.DateTimeField(blank=False, null=False)
    vote_end_date = models.DateTimeField(blank=False, null=False)
    is_closed = models.BooleanField(default=False)


class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, blank=False, null=False, unique=True
    )

    # Spotify data
    spotify_uri = models.CharField(max_length=255, blank=True, null=True)
    spotify_url = models.CharField(max_length=255, blank=True, null=True)

    # Boolean field to check if artist is from spotify
    is_non_spotify = models.BooleanField(default=False)


class Track(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=False, null=False)
    artists = models.ManyToManyField(Artist)

    # Spotify data
    spotify_uri = models.CharField(max_length=255, blank=True, null=True)
    preview_url = models.CharField(max_length=255, blank=True, null=True)
    spotify_url = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)

    # Boolean field to check if track is from spotify
    is_non_spotify = models.BooleanField(default=False)


class VoteSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submitter_name = models.CharField(max_length=255, blank=False, null=False)
    is_invalidated = models.BooleanField(default=False)


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(
        Track, blank=False, null=False, on_delete=models.PROTECT
    )
    submission = models.ForeignKey(
        VoteSubmission, blank=False, null=False, on_delete=models.CASCADE
    )
    points = models.PositiveIntegerField(blank=False, null=False)
