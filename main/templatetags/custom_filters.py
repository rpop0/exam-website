from django import template
from users.utils.position_manager import position_list

register = template.Library()


@register.filter("position_translate")
def position_id_to_string(position_id):
    if position_list[position_id]:
        return position_list[position_id]
    return "Unknown position"

@register.filter('key')
def key(dictionary, key_name):
    return dictionary[key_name]
