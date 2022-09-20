from dataclasses import asdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.utils.translation import activate

from core.forms import VoteSubmissionForm
from core.models import VoteSubmission
from core.spotify import spotify


class IndexView(TemplateView):
    template_name = "index.html"


class VoteView(View):
    template_name = "vote.html"

    def get(self, request, *args, **kwargs):
        return render(
            request, self.template_name, {"voteForm": VoteSubmissionForm()}
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
        return render(request, self.template_name, {"voteForm": form})


class VoteSubmissionDetailView(DetailView):
    template_name = "view_vote_submission.html"
    model = VoteSubmission

    def get_queryset(self):
        return (
            super().get_queryset().prefetch_related("vote_set__track__artists")
        )


class SpotipySearchView(View):
    def get(self, request, *args, **kwargs):
        q = request.GET.get("q")
        return JsonResponse(
            {
                "results": list(
                    map(lambda x: asdict(x), spotify.search_tracks(q))
                )
            }
        )


class SpotipyGetView(View):
    def get(self, request, spotifyuri, *args, **kwargs):
        return JsonResponse(asdict(spotify.get_track_by_uri(spotifyuri)))


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/base.html"
