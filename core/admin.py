from django.contrib import admin

from core.models import HitList, Artist, Track, VoteSubmission, Vote

admin.site.register(HitList)
admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(VoteSubmission)
admin.site.register(Vote)
