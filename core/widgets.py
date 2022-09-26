from django.forms import DateTimeInput


class CustomDateTimeInput(DateTimeInput):
    input_type = "datetime-local"
