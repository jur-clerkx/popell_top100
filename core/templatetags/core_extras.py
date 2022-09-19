from django import template

register = template.Library()


@register.filter
def artist_list(value):
    return ", ".join(map(lambda artist: artist.name, value))
