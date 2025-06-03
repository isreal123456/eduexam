from django import template
register = template.Library()

@register.filter
def get_item_as_p(forms_dict, key):
    form = forms_dict.get(key)
    if form:
        return form.as_p()
    return ""
