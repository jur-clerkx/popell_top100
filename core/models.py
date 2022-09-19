import uuid

from django.db import models, transaction

from core.spotify import spotify


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
    spotify_uri = models.CharField(
        max_length=255, blank=True, null=True, unique=True
    )
    spotify_url = models.CharField(max_length=255, blank=True, null=True)

    # Boolean field to check if artist is from spotify
    is_non_spotify = models.BooleanField(default=False)

    @staticmethod
    def get_or_create_artist_by_uri(artist_uri):
        try:
            return Artist.objects.get(spotify_uri=artist_uri)
        except models.ObjectDoesNotExist:  # Create artist in the database
            artist_json = spotify.get_artist_by_uri(artist_uri)
            artist = Artist(
                name=artist_json.name,
                spotify_uri=artist_json.id,
                spotify_url=artist_json.spotify_url,
                is_non_spotify=False,
            )
            artist.save()
            return artist


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

    @staticmethod
    def get_or_create_song_by_uri(song_uri):
        try:
            return Track.objects.get(spotify_uri=song_uri)
        except models.ObjectDoesNotExist:  # Create track in the database
            track_json = spotify.get_track_by_uri(song_uri)
            artists = []
            for artist_json in track_json.track_artists:
                artists.append(
                    Artist.get_or_create_artist_by_uri(artist_json.id)
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

    def __str__(self):
        return self.title


class VoteSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submitter_name = models.CharField(max_length=255, blank=False, null=False)
    is_invalidated = models.BooleanField(default=False)

    @staticmethod
    @transaction.atomic
    def create_vote_submission(
        name, song_1_uri, song_2_uri, song_3_uri, song_4_uri, song_5_uri
    ):
        submission = VoteSubmission(submitter_name=name)
        submission.save()
        Vote.objects.create(
            track=Track.get_or_create_song_by_uri(song_1_uri),
            submission=submission,
            points=5,
        )
        Vote.objects.create(
            track=Track.get_or_create_song_by_uri(song_2_uri),
            submission=submission,
            points=4,
        )
        Vote.objects.create(
            track=Track.get_or_create_song_by_uri(song_3_uri),
            submission=submission,
            points=3,
        )
        Vote.objects.create(
            track=Track.get_or_create_song_by_uri(song_4_uri),
            submission=submission,
            points=2,
        )
        Vote.objects.create(
            track=Track.get_or_create_song_by_uri(song_5_uri),
            submission=submission,
            points=1,
        )
        return submission


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(
        Track, blank=False, null=False, on_delete=models.PROTECT
    )
    submission = models.ForeignKey(
        VoteSubmission, blank=False, null=False, on_delete=models.CASCADE
    )
    points = models.PositiveIntegerField(blank=False, null=False)
