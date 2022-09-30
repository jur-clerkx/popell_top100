from django.forms import DateTimeInput
from django_select2 import forms as s2forms


class CustomDateTimeInput(DateTimeInput):
    input_type = "datetime-local"


class TrackSelectWidget(s2forms.Select2Widget):
    search_fields = [
        "title__icontains",
        "artists__name__icontains",
    ]
