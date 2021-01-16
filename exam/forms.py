from django import forms
from exam.models import Question, Answer, ExamTemplate, Exam
from exam.utils.sections import translate_choices

class ManageQuestionsForm(forms.ModelForm):

    category_choices = [
        (0, "Multiple Choice"),
        (1, "Open Answers")
    ]

    type_choices = [
        (0, "Multiple choice"),
        (1, "True/False"),
        (2, "Open response")
    ]

    category = forms.ChoiceField(widget=forms.Select, choices=category_choices)
    question_type = forms.ChoiceField(widget=forms.Select, choices=type_choices)
    class Meta:
        model = Question
        fields = ['question', 'question_type', 'category', 'point_value']


class ManageAnswersForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        question_id = kwargs.pop('pk', None)
        super(ManageAnswersForm, self).__init__(*args, **kwargs)
        if question_id:
            question = Question.objects.filter(pk=question_id).first()
            if question.question_type == 2:
                self.fields['answer'] = forms.CharField(widget=forms.Textarea)
                self.fields['correct'] = forms.BooleanField(widget=forms.HiddenInput, initial=False, required=False)
            else:
                self.fields['answer'] = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = Answer
        fields = ['answer', 'correct']




class ManageExamsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): #To dynamically split the questions per section in this part, I need to take the split questions as arguments
        s_one = kwargs.pop('section_one', None) #This gets the section 1 questions, the values are given as a function argument
        s_two = kwargs.pop('section_two', None) #This gets the section 2 questions.

        super(ManageExamsForm, self).__init__(*args, **kwargs)
        if s_one: #If it's set, set the choices field of the section_one form entry to the argument given
            self.fields['questions_one'].choices = s_one
        if s_two:
            self.fields['questions_two'].choices = s_two


    class Meta:
        model = ExamTemplate
        fields = ['exam_name', "questions_one", "questions_two"]
        widgets = {
            "questions_one": forms.CheckboxSelectMultiple,
            "questions_two": forms.CheckboxSelectMultiple,
        }
        labels = {
            "questions_one": '',
            "questions_two": ''
        }


class ExamForm(forms.ModelForm):
    full_name = forms.CharField(max_length=64)
    class Meta:
        model = Exam
        fields = ['exam_template']
