import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

register = template.Library()


JSON_TAG_ESCAPES = {
    '>': '\\u003E',
    '<': '\\u003C',
    '&': '\\u0026',
}


@register.filter(name='json', is_safe=True)
def json_filter(value):
    text = json.dumps(value, cls=DjangoJSONEncoder)
    for char, to in JSON_TAG_ESCAPES.items():
        text = text.replace(char, to)
    return mark_safe(text.replace('"', '&quot;'))
