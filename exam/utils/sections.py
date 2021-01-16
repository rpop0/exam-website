from exam.models import Question


def translate_choices(choice):
    if choice == 0:
        return "Multiple Choice"
    return "Open Answers"



def get_questions(category_id):
    choices = list()
    questions = Question.objects.filter(category=category_id)
    for question in questions:
        if question.answer_set.first():
            choices.append((question.id, question.question))
    return choices