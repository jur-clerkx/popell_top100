from django.db import models


class HitListSettings(models.Model):
    current_hitlist = models.ForeignKey(
        "HitList", on_delete=models.deletion.CASCADE
    )
