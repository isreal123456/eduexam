from django import template

register = template.Library()

@register.filter
def percentage(score, total):
    try:
        return (score / total) * 100
    except (ZeroDivisionError, TypeError):
        return 0
