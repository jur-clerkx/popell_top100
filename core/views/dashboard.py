import logging
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    FormView,
    DeleteView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from core.forms import MergeTracksForm
from core.models.music import Track
from core.models.voting import HitList, VoteSubmission
from core.services.music import SimilarTrackService
from core.services.settings import SettingsService
from core.services.voting import HitListService
from core.spotify import spotify
from core.widgets import CustomDateTimeInput
from tinymce.widgets import TinyMCE  # type: ignore

HITLIST_LIST_URL = "core:hitlist-list"
DASHBOARD_URL = "core:dashboard"


logger = logging.getLogger(__name__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):
        if "list" in request.GET:
            hitlist = get_object_or_404(HitList, id=request.GET["list"])
            SettingsService.set_current_hitlist(request, hitlist)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["hitlists"] = HitList.objects.all()
        ctx["hitlist"] = SettingsService.get_current_hitlist(self.request)
        ctx["vote_count"] = VoteSubmission.objects.filter(
            hit_list=ctx["hitlist"], is_invalidated=False
        ).count()
        ctx["invalidated"] = VoteSubmission.objects.filter(
            hit_list=ctx["hitlist"], is_invalidated=True
        ).count()
        return ctx


class HistListListView(LoginRequiredMixin, ListView):
    model = HitList
    template_name = "dashboard/cms/hitlistlist.html"


class SimilarTrackView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/cms/similartracks.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["similar_tracks"] = SimilarTrackService.get_similar_tracks()
        return ctx


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
