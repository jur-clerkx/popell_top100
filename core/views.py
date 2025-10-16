from dataclasses import asdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView,
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
)
from django.utils.translation import activate
import logging

from rapidfuzz.fuzz import QRatio
from thefuzz import process
from tinymce.widgets import TinyMCE

from core.forms import VoteSubmissionForm, CustomTrackForm, MergeTracksForm
from core.models.voting import VoteSubmission, HitList, Vote
from core.models.tracks import Track
from core.services.settings import SettingsService
from core.services.voting import HitListService
from core.spotify import spotify
from core.widgets import CustomDateTimeInput

logger = logging.getLogger(__name__)

HITLIST_LIST_URL = "core:hitlist-list"
DASHBOARD_URL = "core:dashboard"


class OpenHitListRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if (
                not HitListService.get_current_hitlist()
                or HitListService.get_current_hitlist().is_closed
        ):
            return redirect("core:closed")
        return super().dispatch(request, *args, **kwargs)


class IndexView(OpenHitListRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hitlist"] = HitListService.get_current_hitlist()
        return context


class HitlistClosedView(TemplateView):
    template_name = "closed.html"


class VoteView(OpenHitListRequiredMixin, View):
    template_name = "vote.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "voteForm": VoteSubmissionForm(),
                "hitlist": HitListService.get_current_hitlist(),
            },
        )

    def post(self, request, *args, **kwargs):
        activate("nl")  # Make sure errors are displayed in correct language
        form = VoteSubmissionForm(request.POST)
        if (
                form.is_valid()
        ):  # Valid submission, save and redirect to detail page
            vote_submission = form.save()
            return redirect(
                reverse(
                    "core:vote-submission-detail",
                    kwargs={"pk": vote_submission.id},
                )
            )
        return render(
            request,
            self.template_name,
            {
                "voteForm": form,
                "hitlist": SettingsService.get_current_hitlist(),
            },
        )


class VoteSubmissionDetailView(DetailView):
    template_name = "view_vote_submission.html"
    model = VoteSubmission

    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related("vote_set__track__artists")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vote = self.get_object()
        context["hitlist"] = vote.hit_list
        return context


class AddCustomTrackView(FormView):
    form_class = CustomTrackForm
    template_name = "add_custom_song.html"
    success_url = reverse_lazy("core:add-custom-track-success")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hitlist"] = HitListService.get_current_hitlist()
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AddCustomTrackSuccessView(TemplateView):
    template_name = "add_custom_song_success.html"


class SpotipySearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q")
        search_results = spotify.search_custom_tracks(
            q
        ) + spotify.search_tracks(q)
        return JsonResponse(
            {"results": list(map(lambda x: asdict(x), search_results))}
        )


class SpotipyGetView(View):
    def get(self, request, spotifyuri, *args, **kwargs):
        return JsonResponse(asdict(spotify.get_track_by_uri(spotifyuri)))


class TrackStatsGetView(View):
    def get(self, request, *args, **kwargs):
        title = request.GET.get("title", "")
        year = request.GET.get("year", "")
        artist = request.GET.get("artist", "")
        track_uri = request.GET.get("spotify_uri", "")
        print(title, year, artist, track_uri)
        hitlist = HitListService.get_by_year(year)
        track = Track.find_by_uri_or_title(track_uri, title)
        if track is None:
            return JsonResponse(status=404, data={"error": "Track not found!"})
        votes = Vote.objects.filter(track=track, submission__hit_list=hitlist, submission__is_invalidated=False)
        if votes.count() == 0:
            return JsonResponse(status=404, data={"error": "Track not part of hitlist!"})
        position = 1
        for entry in hitlist.get_list():
            if entry.id == track.id:
                break
            position += 1
        vote_count, points = 0, 0
        for vote in votes:
            vote_count += 1
            points += vote.points
        votes = VoteSubmission.objects.filter(
            hit_list=hitlist, vote__track=track, is_invalidated=False
        ).values("submitter_name")
        return JsonResponse(
            {
                "track": str(track),
                "position": position,
                "points": points,
                "number_of_votes": vote_count,
                "voters": list(votes),
            }
        )


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["hitlists"] = HitList.objects.all()
        ctx["hitlist"] = SettingsService.get_current_hitlist()
        ctx["vote_count"] = VoteSubmission.objects.filter(
            hit_list=ctx["hitlist"], is_invalidated=False
        ).count()
        ctx["invalidated"] = VoteSubmission.objects.filter(
            hit_list=ctx["hitlist"], is_invalidated=True
        ).count()
        return ctx

class SimilarTrackView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/cms/similartracks.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        track_names = [t.full_track_string for t in Track.objects.all()]
        results = []
        for track_name in track_names:
            match_list = list(track_names)
            match_list.remove(track_name)
            fuzz = process.extract(track_name, match_list, scorer=QRatio, limit=3)
            for match_name, score in fuzz:
                if score > 70:
                    results.append((track_name, match_name, score))

        ctx["similar_tracks"] = results
        return ctx


class HistListListView(LoginRequiredMixin, ListView):
    model = HitList
    template_name = "dashboard/cms/hitlistlist.html"


class HitListCreateView(LoginRequiredMixin, CreateView):
    model = HitList
    template_name = "dashboard/cms/hitlistcreate.html"
    fields = [
        "name",
        "vote_start_date",
        "vote_end_date",
        "description",
        "theme",
    ]
    success_url = reverse_lazy(HITLIST_LIST_URL)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["vote_start_date"].widget = CustomDateTimeInput()
        form.fields["vote_end_date"].widget = CustomDateTimeInput()
        form.fields["description"].widget = TinyMCE()
        return form


class HitListUpdateView(LoginRequiredMixin, UpdateView):
    model = HitList
    template_name = "dashboard/cms/hitlistupdate.html"
    fields = [
        "name",
        "vote_start_date",
        "vote_end_date",
        "description",
        "theme",
        "is_closed",
    ]
    success_url = reverse_lazy(HITLIST_LIST_URL)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["vote_start_date"].widget = CustomDateTimeInput()
        form.fields["vote_end_date"].widget = CustomDateTimeInput()
        form.fields["description"].widget = TinyMCE()
        return form


class HitListDeleteView(LoginRequiredMixin, DeleteView):
    model = HitList
    success_url = reverse_lazy(HITLIST_LIST_URL)
    template_name = "dashboard/cms/hitlistdelete.html"


class HitListExportView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        hitlist = get_object_or_404(HitList, id=pk)
        return HitListService.export_to_excel(hitlist)


class CustomTrackListView(LoginRequiredMixin, ListView):
    model = Track
    template_name = "dashboard/cms/tracklist.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("artists")
            .filter(is_non_spotify=True)
        )


class CustomTrackUpdateView(LoginRequiredMixin, UpdateView):
    model = Track
    template_name = "dashboard/cms/trackupdate.html"
    fields = ["title", "artists", "preview_url", "image_url"]
    success_url = reverse_lazy("core:custom-track-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["artists"].queryset = form.fields[
            "artists"
        ].queryset.filter(is_non_spotify=True)
        return form


class MergeTracksView(LoginRequiredMixin, FormView):
    form_class = MergeTracksForm
    template_name = "dashboard/cms/mergetracks.html"
    success_url = reverse_lazy(HITLIST_LIST_URL)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ToggleSubmissionInvalidation(LoginRequiredMixin, View):
    def get(self, request, votesubmissionid, *args, **kwargs):
        submission = VoteSubmission.objects.get(id=votesubmissionid)
        submission.is_invalidated = not submission.is_invalidated
        submission.save()
        return redirect(reverse_lazy(DASHBOARD_URL))


class HitListCreateSpotifyPlaylistView(View):
    def get(self, request, hitlist_id, *args, **kwargs):
        hitlist = get_object_or_404(HitList, id=hitlist_id)
        try:
            HitListService.create_spotify_list(
                hitlist, request.session.get("spotify_token")
            )
        except Exception as e:
            logger.error("Failed to create spotify playlist!")
            logger.error(e)
            request.session["spotify_token"] = None
        return redirect(reverse_lazy(DASHBOARD_URL))


class SpotifyOAuthView(View):
    def get(self, request):
        spotify_oauth = spotify.get_spotify_oauth()
        callback_code = request.GET.get("code", None)
        if callback_code:
            # Found callback code, add access token to session
            access_token = spotify_oauth.get_access_token(callback_code)[
                "access_token"
            ]
            request.session["spotify_token"] = access_token
            return redirect(reverse_lazy(DASHBOARD_URL))
        else:
            return redirect(spotify_oauth.get_authorize_url())
