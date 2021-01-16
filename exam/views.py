from collections import Counter
from json import loads 

from django.shortcuts import redirect, reverse, get_object_or_404, render
from django.views.generic import TemplateView, ListView, DeleteView, FormView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import F

from main.utils.mixins import UserIsStaffMixin, UserIsSeniorMixin
from exam.forms import ManageQuestionsForm, ManageAnswersForm, ManageExamsForm, ExamForm
from exam.models import Question, Answer, ExamTemplate, Exam, Response
from exam.utils.sections import get_questions
from exam.utils.exam import generate_key





class ManageExamsView(LoginRequiredMixin, UserIsSeniorMixin, TemplateView):
    template_name = 'exam/manage-exams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context

class EditQuestionsListView(LoginRequiredMixin, UserIsStaffMixin, ListView):
    model = Question
    context_object_name = 'question_list'
    form = ManageQuestionsForm
    template_name = 'exam/edit-questions.html'
    ordering = ['-creation_date']
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            form.save()
        return redirect('exam-edit-questions')

class EditQuestionsUpdateView(LoginRequiredMixin, UserIsStaffMixin, SuccessMessageMixin, UpdateView):
    model = Question
    form_class = ManageQuestionsForm
    template_name = 'exam/edit-questions-update.html'
    success_message = 'Question updated'
    allow_empty = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context
    def get_success_url(self):
        return reverse('exam-edit-questions-update', kwargs={'pk': self.kwargs['pk']})
    success_url = get_success_url

class EditQuestionsDeleteView(LoginRequiredMixin, UserIsStaffMixin, DeleteView):
    model = Question
    template_name = 'exam/edit-questions-delete.html'
    success_url = '/exam/manage/questions'
    allow_empty = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context

class ManageAnswersListView(LoginRequiredMixin, UserIsStaffMixin, ListView):
    model = Answer
    context_object_name = 'answer_list'
    form = ManageAnswersForm
    template_name = 'exam/manage-answers.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        context['question_id'] = self.kwargs['pk']
        context['question_text'] = Question.objects.filter(id=self.kwargs['pk']).first().question
        context['form'] = ManageAnswersForm(pk=self.kwargs['pk'])
        return context

    
    def get_queryset(self): #Need to do this to get a list of answers based on the PK in the url
        question_id = self.kwargs['pk'] #So I get the question ID from the url
        question = Question.objects.filter(id=question_id).first() #Get the first question with that id
        return Answer.objects.filter(question=question).order_by("answer") #And return the answers that have that question

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, pk=self.kwargs['pk'])
        question_id = self.kwargs['pk'] #So I get the question ID from the url
        question = Question.objects.filter(id=question_id).first() #Get the first question with that id
        if form.is_valid():
            new_form = form.save(commit=False) #Using this to populate other fields with data, which is the actual question
            new_form.question = question
            new_form.save()
        return HttpResponseRedirect(self.request.path_info) #Using this since it redirects me to the same page

class ManageAnswersUpdateView(LoginRequiredMixin, UserIsStaffMixin, SuccessMessageMixin, UpdateView):
    model = Answer
    form_class = ManageAnswersForm
    template_name = 'exam/manage-answers-update.html'
    success_message = 'Answer updated'
    allow_empty = False
    def get_form_kwargs(self):
        kwargs = super(ManageAnswersUpdateView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        context['question_id'] = self.kwargs['pk']
        return context
    def get_success_url(self):
        return reverse('exam-manage-answers-update', kwargs={'pk': self.kwargs['pk'], 'aid':self.kwargs['aid']})
    success_url = get_success_url
    def get_object(self, queryset=None):
        return Answer.objects.get(id=self.kwargs['aid'])

class ManageAnswersDeleteView(LoginRequiredMixin, UserIsStaffMixin, DeleteView):
    model = Answer
    template_name = 'exam/manage-answers-delete.html'
    pk_url_kwarg = 'aid'
    allow_empty = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        context['question_id'] = self.kwargs['pk']
        return context
    def get_success_url(self, **kwargs):
        return reverse_lazy('exam-manage-answers', kwargs={'pk': self.kwargs['pk']})

class EditExamsListView(LoginRequiredMixin, UserIsStaffMixin, ListView):
    model = ExamTemplate
    context_object_name = 'exam_list'
    form = ManageExamsForm
    template_name = 'exam/edit-exams.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
        return redirect('exam-edit-exams')

class EditExamsUpdateView(LoginRequiredMixin, UserIsStaffMixin, SuccessMessageMixin, UpdateView):
    model = ExamTemplate
    form_class = ManageExamsForm
    template_name = 'exam/edit-exams-update.html'
    success_message = 'Exam updated'
    allow_empty = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context
    def get_success_url(self):
        return reverse('exam-edit-exams-update', kwargs={'pk': self.kwargs['pk']})  
    success_url = get_success_url
    def get_form_kwargs(self):
        kwargs = super(EditExamsUpdateView, self).get_form_kwargs()
        kwargs['section_one'] = get_questions(0)
        kwargs['section_two'] = get_questions(1)
        return kwargs

class EditExamsDeleteView(LoginRequiredMixin, UserIsStaffMixin, DeleteView):
    model = ExamTemplate
    template_name = 'exam/edit-exams-delete.html'
    success_url = '/exam/manage/exams'
    allow_empty = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context

class EditExamsDetailView(LoginRequiredMixin, UserIsStaffMixin, DetailView):
    model = ExamTemplate
    context_object_name = 'exam'
    template_name = 'exam/edit-exams-view.html'
    allow_empty = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context

class PreExamTemplateView(TemplateView):
    template_name = "exam/pre-exam.html"
    key = None
    
    def get(self, request, *args, **kwargs):
        if 'data' in request.GET:
            self.key = request.GET['data']
            return super().get(request=request, *args, **kwargs) 
        return Http404
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = self.key
        return context

class PostExamTemplateView(TemplateView):
    template_name = "exam/post-exam.html"
        

class ExamFormView(TemplateView):
    template_name = "exam/exam.html"
    model = None
    def get(self, request, *args, **kwargs): #Gets called at the start of the page
        if  'data' in request.GET:  # Checks if there is a GET argument named data
            exam_key = request.GET['data'] #if it is, save it
            requested_exam = get_object_or_404(Exam, key=exam_key, expired=False, passed=False, archived=False, turned_in=None) #Check if there is an exam with that id that is available
            requested_exam_template = requested_exam.exam_template #Get the exam template
            self.model = requested_exam_template #Set the model to the temlate
            current_datetime = timezone.now()
            elapsed = current_datetime - requested_exam.date_sent
            if elapsed.total_seconds() > 172800:
                requested_exam.expired = True
                requested_exam.save()
                raise Http404
            return super().get(request=request, *args, **kwargs) #continue
        raise Http404 #No get argument, 404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exam'] = self.model
        context['questions_one'] = self.model.questions_one.all()
        context['questions_two'] = self.model.questions_two.all()

        return context

    def post(self, request, *args, **kwargs):
        #Here we get the exam so we can update it later
        requested_exam = get_object_or_404(Exam, key=request.GET['data'], expired=False, passed=False, archived=False, turned_in=None)
        answer_list = request.POST.lists() #Grab the answers from the form as a list, index 0 being question, index 1 being answers
        next(answer_list) #Skipping over first element because it's CSRF Tokken
        point_counter = 0 # Start point counting
        question_found = True
        for item in answer_list: # Looping over everyo question
            question = Question.objects.filter(id=item[0]).first() #Getting the actual object for that question
            if question:
                if question.question_type == 2: #If it's a open response, just save the answer, item[1][0] to the database
                    open_response = item[1][0]
                    if question.category == 4: # IF ITS SHORT ANSWER, APPEND S AT THE END
                        open_response = f"{open_response}S"
                    else:
                        open_response = f"{open_response}L" #IF NOT, APPEND L
                    response_entry = Response(exam=requested_exam, open_response=open_response, question=question, answer=question.answer_set.first())
                    response_entry.save()
                else: #If it's not, assume the answer is correct
                    correct = True
                    for element in item[1]: #Loop through all the answers for the current question named item
                        answer = question.answer_set.filter(answer=element).first() #Get the answer object that corresponds to the current answer
                        if answer.correct is False: #Since current answer is assmued as true, if the actual answer is false, the answer is wrong
                            correct = False
                        response_entry = Response(exam=requested_exam, answer=Answer.objects.filter(answer=element).first(), correct=correct, question=question) #Create response
                        response_entry.save() #Create response
                    answers = question.answer_set.filter(correct=True) # Get all the correct answers
                    correct_answers = list()
                    for answer in answers: #Add them in a list
                        correct_answers.append(answer.answer)
                    if Counter(correct_answers) == Counter(item[1]): #Check if the correct answers list is the guy's answers
                        point_counter += question.point_value
                    #Save it
            else:
                question_found = False
        if question_found:
            requested_exam.points = point_counter #Update the exam to reflect points and turned in
            requested_exam.turned_in = timezone.now()
            requested_exam.save()
            return redirect('exam-done')
        return redirect(f'{request.path}?data={request.GET["data"]}') # question not found.


class ActiveExamsListView(LoginRequiredMixin, UserIsSeniorMixin, ListView):
    model = Exam
    template_name = "exam/active-exams.html"
    context_object_name = "exam_list"
    form = ExamForm

    def get_queryset(self):
        return Exam.objects.filter(archived=False).order_by('-date_sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        context['form'] = self.form
        return context
    def post(self, request, *args, **kwargs):
        if request.is_ajax(): # If the request is ajax
            payload = loads(request.body) #Get the body of the request
            exam = Exam.objects.filter(key=payload['key']).first() #Grab the exam that has that key
            exam.archived = True #Set the exam as archived and respond.
            exam.save()
            return JsonResponse({"Archived": True}, status=200)

        form = self.form(request.POST) #Get the form from the page
        if form.is_valid():
            full_name = form.cleaned_data['full_name'].split(" ")
            key = generate_key(full_name[0], full_name[1]) #Generate the key
            exam = Exam( #Create the exam
                first_name=full_name[0],
                last_name=full_name[1],
                key=key,
                exam_template=form.cleaned_data['exam_template']
                )
            exam.save()
            
        return redirect('exam-active')


class ExamsListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = "exam/exams-view.html"
    context_object_name = "exam_list"

    def get_queryset(self):
        return Exam.objects.filter(archived=False).order_by(F('turned_in').desc(nulls_last=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'exams'
        return context

    def post(self, request, *args, **kwargs):
        if 'handle' in request.POST:
            exam = Exam.objects.filter(key=request.POST['handle']).first()
            exam.handler = request.user
            exam.save()
        elif 'unhandle' in request.POST:
            exam = Exam.objects.filter(key=request.POST['unhandle']).first()
            exam.handler = None
            exam.save()
        return redirect('exams-view')

class ExamReviewDetailView(LoginRequiredMixin, DetailView):
    model = Exam
    context_object_name = 'exam'
    template_name = 'exam/exams-review.html'
    allow_empty = False
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'exam'
        return context

    def post(self, request, *args, **kwargs):
        if request.POST:
            exam = Exam.objects.filter(pk=self.kwargs['pk']).first() #Get the exam
            response_list = request.POST.lists() #Get all the fields
            next(response_list) #skip csrf token
            for response_key in response_list: #Loop through responses
                if "points" in response_key[0] or "review" in response_key[0]: #If the response has the format points- or review-
                    response_id = response_key[0].split("-")[1] #Grabs the response ID from the points-(ID) fpr,at
                    if 'review' in response_key[0]: #If it's the review part, save it to the database
                        response_object = Response.objects.filter(pk=response_id).first()
                        response_object.review = response_key[1][0]
                        response_object.save()
                    elif 'points' in response_key[0]: #if it's the points, save them as well
                        response_object = Response.objects.filter(pk=response_id).first()
                        response_object.open_response_points = int(response_key[1][0])
                        response_object.save()
            exam.points_open_response = int(request.POST['final-grade']) - int(exam.points) #Save the open response points, they are final grade minus the current points
            if 'mark' in request.POST:
                point_name = "RED - Marking Examination"
                exam.marked = True #set it as marked
                exam.handler = None
                exam.marked_by = f"{request.user.first_name} {request.user.last_name}"
            else:
                point_name = "RED - Reviewing Examination"
                if 'pass' in request.POST:
                    exam.reviewed = True
                    exam.passed = True
                elif 'fail' in request.POST:
                    exam.reviewed = True
                    exam.passed = False
            exam.save()

        return HttpResponseRedirect(self.request.path_info)

class ArchivedExamsListView(LoginRequiredMixin, UserIsSeniorMixin, ListView):
    model = Exam
    template_name = "exam/archived-exams.html"
    context_object_name = "exam_list"

    def get_queryset(self):
        return Exam.objects.filter(archived=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context
