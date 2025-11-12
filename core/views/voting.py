from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from core.forms import CustomTrackForm, VoteSubmissionForm
from core.models.voting import VoteSubmission
from core.services.settings import SettingsService
from core.services.voting import HitListService
from core.views.mixins import OpenHitListRequiredMixin

from django.views.generic import TemplateView, DetailView, FormView
from django.utils.translation import activate


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
