position_list = [
    "Assistant",
    "Lecturer",
    "Associate Professor",
    "Professor",
    ]

def get_position_list_choices():
    choices = list()
    for idx, val in enumerate(position_list):
        choices.append((idx, val))
    return choices