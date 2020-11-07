from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter(name='highlighttitle')
def highlighttitle(text, search):

    for i in search:
        highlighted = re.sub(i, '<big><span class="badge badge-pill badge-success">{}</span></big>'.format(i), text, flags=re.IGNORECASE)
        text = highlighted
    return mark_safe(text)


@register.filter(name='highlightspecification')
def highlightspecification(text, search):

    for i in search:
        highlighted = re.sub(i, '<big><span class="badge badge-pill badge-secondary">{}</span></big>'.format(i), text, flags=re.IGNORECASE)
        text = highlighted
    return mark_safe(text)
