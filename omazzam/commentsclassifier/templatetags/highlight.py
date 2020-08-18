from django import template
from django.utils.safestring import mark_safe
import re

register = template.Library()


@register.filter(name='highlightpredefined')
def highlightpredefined(text, search):

    for i in search:
        highlighted = re.sub(i, '<big><span class="badge badge-pill badge-success">{}</span></big>'.format(i), text, flags=re.IGNORECASE)
        text = highlighted
    return mark_safe(text)


@register.filter(name='highlightuser')
def highlightuser(text, search):

    for i in search:
        highlighted = re.sub(i, '<big><span class="badge badge-pill badge-secondary" style="fontSize:16px;" >{}</span></big>'.format(i), text, flags=re.IGNORECASE)
        text = highlighted
    return mark_safe(text)
