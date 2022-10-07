from dataclasses import asdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
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

from core.forms import VoteSubmissionForm, CustomTrackForm, MergeTracksForm
from core.models import VoteSubmission, HitList, Track
from core.spotify import spotify
from core.widgets import CustomDateTimeInput


class OpenHitListRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not HitList.get_current_hitlist():
            return redirect("core:closed")
        return super().dispatch(request, *args, **kwargs)


class IndexView(OpenHitListRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hitlist"] = HitList.get_current_hitlist()
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
                "hitlist": HitList.get_current_hitlist(),
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
            {"voteForm": form, "hitlist": HitList.get_current_hitlist()},
        )


class VoteSubmissionDetailView(DetailView):
    template_name = "view_vote_submission.html"
    model = VoteSubmission

    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related("vote_set__track__artists")
        )


class AddCustomTrackView(FormView):
    form_class = CustomTrackForm
    template_name = "add_custom_song.html"
    success_url = reverse_lazy("core:add-custom-track-success")

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


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        arg = self.request.GET.get("list", None)
        if arg:
            try:
                ctx["hitlist"] = HitList.objects.get(pk=arg)
            except Exception:
                ctx["hitlist"] = HitList.get_current_hitlist()
        else:
            ctx["hitlist"] = HitList.get_current_hitlist()
        ctx["hitlists"] = HitList.objects.all()
        return ctx


class HistListListView(LoginRequiredMixin, ListView):
    model = HitList
    template_name = "dashboard/cms/hitlistlist.html"


class HitListCreateView(LoginRequiredMixin, CreateView):
    model = HitList
    template_name = "dashboard/cms/hitlistcreate.html"
    fields = ["name", "vote_start_date", "vote_end_date"]
    success_url = reverse_lazy("core:hitlist-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["vote_start_date"].widget = CustomDateTimeInput()
        form.fields["vote_end_date"].widget = CustomDateTimeInput()
        return form


class HitListUpdateView(LoginRequiredMixin, UpdateView):
    model = HitList
    template_name = "dashboard/cms/hitlistupdate.html"
    fields = ["name", "vote_start_date", "vote_end_date", "is_closed"]
    success_url = reverse_lazy("core:hitlist-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["vote_start_date"].widget = CustomDateTimeInput()
        form.fields["vote_end_date"].widget = CustomDateTimeInput()
        return form


class HitListDeleteView(LoginRequiredMixin, DeleteView):
    model = HitList
    success_url = reverse_lazy("core:hitlist-list")
    template_name = "dashboard/cms/hitlistdelete.html"


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
    success_url = reverse_lazy("core:dashboard")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ToggleSubmissionInvalidation(LoginRequiredMixin, View):
    def get(self, request, votesubmissionid, *args, **kwargs):
        submission = VoteSubmission.objects.get(id=votesubmissionid)
        submission.is_invalidated = not submission.is_invalidated
        submission.save()
        return redirect(reverse_lazy("core:dashboard"))


class HitListCreateSpotifyPlaylistView(View):
    def get(self, request, hitlist_id, *args, **kwargs):
        hitlist = get_object_or_404(HitList, id=hitlist_id)
        hitlist.create_spotify_list()
        return redirect(reverse_lazy("core:dashboard"))
