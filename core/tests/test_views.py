from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from datetime import datetime, timedelta

from core.models.voting import HitList
from core.views import IndexView, VoteView


def get_hit_list():
    yesterday = datetime.now() - timedelta(days=1)
    tomorrow = datetime.now() + timedelta(days=1)
    hitlist = HitList.objects.create(
        name="Test list",
        vote_start_date=yesterday,
        vote_end_date=tomorrow,
    )
    return hitlist


def get_closed_hit_list():
    hitlist = get_hit_list()
    hitlist.is_closed = True
    hitlist.save()
    return hitlist


def get_passed_hitlist():
    hitlist = get_hit_list()
    passed_time = datetime.now() - timedelta(hours=4)
    hitlist.vote_end_date = passed_time
    hitlist.save()
    return hitlist


class IndexViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("core:index")

    def test_no_hitlist_available(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()

        response = IndexView.as_view()(request)
        self.assertRedirects(
            response, reverse("core:closed"), fetch_redirect_response=False
        )

    def test_hitlist_available(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        hitlist = get_hit_list()
        response = IndexView.as_view()(request)
        self.assertInHTML(
            "<h1>" + hitlist.name + "</h1>", response.rendered_content
        )

    def test_hitlist_closed(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        get_closed_hit_list()
        response = IndexView.as_view()(request)
        self.assertRedirects(
            response, reverse("core:closed"), fetch_redirect_response=False
        )

    def test_hitlist_passed(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        get_passed_hitlist()
        response = IndexView.as_view()(request)
        self.assertRedirects(
            response, reverse("core:closed"), fetch_redirect_response=False
        )


class VoteViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("core:vote")

    def test_no_hitlist_available(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()

        response = VoteView.as_view()(request)
        self.assertRedirects(
            response, reverse("core:closed"), fetch_redirect_response=False
        )

    def test_hitlist_available(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        hitlist = get_hit_list()
        response = VoteView.as_view()(request)
        self.assertInHTML(
            "<h2>" + hitlist.name + " stemformulier</h2>",
            response.content.decode("utf-8"),
        )

    def test_hitlist_closed(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        get_closed_hit_list()
        response = VoteView.as_view()(request)
        self.assertRedirects(
            response, reverse("core:closed"), fetch_redirect_response=False
        )

    def test_hitlist_passed(self):
        request = self.factory.get(self.url)
        request.user = AnonymousUser()
        get_passed_hitlist()
        response = VoteView.as_view()(request)
        self.assertRedirects(
            response, reverse("core:closed"), fetch_redirect_response=False
        )
