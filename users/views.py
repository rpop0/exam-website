from django.shortcuts import redirect, reverse
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from main.utils.mixins import UserIsAdminMixin
from .forms import UserRegisterForm, UserUpdateForm, UserAdminUpdateForm
from .models import RegistrationKey, User

class RegisterView(UserPassesTestMixin, FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        form_key = form.cleaned_data.get('key') #Gets the key from the form
        username = form.cleaned_data.get('username') #Gets the username from the form
        auth_key = RegistrationKey.objects.filter(key=form_key).first() #Queries the database for the authentication key.
        #If it find an authentication key, it means the key is valid. Then we check the first and last name against the ones from the keys table
        if auth_key is not None and auth_key.first_name == form.cleaned_data.get('first_name') and auth_key.last_name == form.cleaned_data.get('last_name'):
            form.save() #Save the user to the database
            new_user = User.objects.filter(username=username).first() #Grab the newly created user object
            new_user.position = auth_key.position #Set it's position
            new_user.save() #Save it to the database
            auth_key.delete() #Deletes the key entry
            return super().form_valid(form)
        return super().form_invalid(form)

    def test_func(self):
        if self.request.user.is_authenticated:
            return False
        return True

    def handle_no_permission(self):
        return redirect('main-dashboard')

class UserSettingsUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/user-settings.html'
    model = User
    context_object_name = 'viewed_user'
    form_class = UserUpdateForm
    success_message = 'User information updated!'

    def test_func(self):
        if self.request.user.id == self.kwargs['pk']:
            return True
        return False

    def handle_no_permission(self):
        return redirect('main-dashboard')

class UserSettingsAdminUpdateView(LoginRequiredMixin, UserIsAdminMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/user-settings.html'
    model = User
    context_object_name = 'viewed_user'
    form_class = UserAdminUpdateForm
    success_message = 'User information updated!'
    def get_success_url(self):
        return reverse('users-manage-settings', kwargs={'pk': self.kwargs['pk']})
    success_url = get_success_url
    