from django.contrib import admin

from core.models.voting import HitList, VoteSubmission, Vote
from core.models.music import Artist, Track
from core.models.settings import HitListSettings

admin.site.register(HitList)
admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(VoteSubmission)
admin.site.register(Vote)
admin.site.register(HitListSettings)
