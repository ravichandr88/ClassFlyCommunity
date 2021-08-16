from django import template

register = template.Library()

@register.simple_tag
def update_variable(value):
    data = value
    return str(data)