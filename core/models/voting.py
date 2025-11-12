import datetime
import uuid

from django.db import models, transaction
from django.db.models import Count, Sum, Min

from core.models.settings import HitListSettings
from core.models.music import Track


class HitList(models.Model):
    THEME_CHOICES = (("rock", "Rock"), ("carnaval", "Carnaval"))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, blank=False, null=False, unique=True
    )
    vote_start_date = models.DateTimeField(blank=False, null=False)
    vote_end_date = models.DateTimeField(blank=False, null=False)
    is_closed = models.BooleanField(default=False)
    description = models.TextField(blank=False, null=False, default="")
    theme = models.CharField(
        max_length=255, choices=THEME_CHOICES, default="rock"
    )

    def get_list(self):
        return (
            Track.objects.filter(
                vote__submission__hit_list=self,
                vote__submission__is_invalidated=False,
            )
            .annotate(
                votes=Count("vote__points"),
                score=Sum("vote__points"),
                first_vote=Min("vote__submission__timestamp"),
            )
            .order_by("-score", "-votes", "first_vote")
            .prefetch_related("artists")
        )


class VoteSubmission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submitter_name = models.CharField(max_length=255, blank=False, null=False)
    is_invalidated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    hit_list = models.ForeignKey(
        HitList, blank=False, null=False, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.submitter_name


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    track = models.ForeignKey(
        Track, blank=False, null=False, on_delete=models.PROTECT
    )
    submission = models.ForeignKey(
        VoteSubmission, blank=False, null=False, on_delete=models.CASCADE
    )
    points = models.PositiveIntegerField(blank=False, null=False)
