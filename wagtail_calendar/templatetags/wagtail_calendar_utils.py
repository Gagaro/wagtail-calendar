import json

from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

register = template.Library()


_json_tag_escapes = {
    ord('>'): '\\u003E',
    ord('<'): '\\u003C',
    ord('&'): '\\u0026',
}


@register.filter(name='json', is_safe=True)
def json_filter(value):
    return mark_safe(json.dumps(value, cls=DjangoJSONEncoder).translate(_json_tag_escapes).replace('"', '&quot;'))
