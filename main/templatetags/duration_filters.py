from django import template

register = template.Library()

@register.filter
def duration_in_minutes(value):
    try:
        return int(value.total_seconds() // 60)
    except:
        return 0