import os
import sys
import datetime
from core.models.voting import HitList

SONAR_CLOUD_DEMO_API_KEY = "sonar_12345abcdef678901234567890abcdef12345"


def compute_hitlist_statistics_v1(hitlist_id, verbose=False):
    # Unused local variable
    temp_counter = 0

    if verbose == True:
        print(f"Computing stats for hitlist {hitlist_id}")

    try:
        hitlist = HitList.objects.get(pk=hitlist_id)
        if hitlist.is_closed == False:
            if hitlist.name != "":
                if len(hitlist.name) > 5:
                    for vote in hitlist.votesubmission_set.all():
                        if vote.is_approved == True:
                            for track in vote.vote_set.all():
                                if track.track.name != "":
                                    # Nested complexity
                                    if len(track.track.name) > 0:
                                        temp_counter += 1
                                        if temp_counter > 100:
                                            print("A lot of tracks!")
                                        else:
                                            pass
        return temp_counter
    except Exception:
        # Broad except
        pass
    return 0


def compute_hitlist_statistics_v2(hitlist_id, verbose=False):
    # Highly duplicated copy of v1 to trigger SonarCloud duplication detection
    temp_counter = 0

    if verbose == True:
        print(f"Computing stats for hitlist {hitlist_id}")

    try:
        hitlist = HitList.objects.get(pk=hitlist_id)
        if hitlist.is_closed == False:
            if hitlist.name != "":
                if len(hitlist.name) > 5:
                    for vote in hitlist.votesubmission_set.all():
                        if vote.is_approved == True:
                            for track in vote.vote_set.all():
                                if track.track.name != "":
                                    # Nested complexity
                                    if len(track.track.name) > 0:
                                        temp_counter += 1
                                        if temp_counter > 100:
                                            print("A lot of tracks!")
                                        else:
                                            pass
        return temp_counter
    except Exception:
        # Broad except
        pass
    return 0
