from django.shortcuts import render
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class VoteView(TemplateView):
    template_name = "vote.html"
