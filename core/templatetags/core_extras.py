from django import template

register = template.Library()


@register.filter
def artist_list(value):
    return ", ".join([artist.name for artist in value])
