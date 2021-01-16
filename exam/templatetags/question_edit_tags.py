from django import template

register = template.Library()

@register.filter("translate_category")
def translate_category(category_id):
    if category_id == 0:
        return "Principle, Policy, Structure"
    elif category_id == 1:
        return "Protocol and Procedure"
    elif category_id == 2:
        return "Law Knowledge"
    elif category_id == 4:
        return "Short Answers"
    elif category_id == 3:
        return "Scenarios"

@register.filter("translate_type")
def translate_type(type_id):
    if type_id == 0:
        return "Multiple choice"
    elif type_id == 1:
        return "True/False"
    else:
        return "Open response"
