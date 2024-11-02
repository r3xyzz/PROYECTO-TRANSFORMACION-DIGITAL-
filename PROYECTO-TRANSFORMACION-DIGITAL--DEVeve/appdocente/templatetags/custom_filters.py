from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, [])

@register.simple_tag
def get_nested_item(dictionary, dia, hora_inicio):
    try:
        return dictionary[dia][hora_inicio]
    except KeyError:
        return "Libre"  # Valor predeterminado si no se encuentra el valor