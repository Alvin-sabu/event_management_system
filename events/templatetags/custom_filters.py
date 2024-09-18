from django import template
from events.models import Event, Department, Fest  # Import your models

register = template.Library()

@register.filter
def get_object_type(value):
    if isinstance(value, Event):
        return 'event'
    elif isinstance(value, Department):
        return 'department'
    elif isinstance(value, Fest):
        return 'fest'
    return 'item'

