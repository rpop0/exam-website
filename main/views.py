from random import getrandbits
from django.shortcuts import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.utils.mixins import UserIsAdminMixin, UserIsStaffMixin, UserIsSeniorMixin
from main.utils.misc import get_monthly_data
from users.models import RegistrationKey
from users.models import User
from users.forms import RegistrationKeyForm


#main pages

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'dashboard'
        context['dashboardData'] = get_monthly_data()
        return context

class AdminView(LoginRequiredMixin, UserIsSeniorMixin, TemplateView):
    template_name = 'main/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context

class InviteListView(LoginRequiredMixin, UserIsStaffMixin, ListView):
    model = RegistrationKey
    context_object_name = 'key_list'
    template_name = 'main/admin-invite-list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context

class InviteView(LoginRequiredMixin, UserIsStaffMixin, TemplateView):
    template_name = 'main/admin-invite.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context

class InviteCreateView(LoginRequiredMixin, UserIsStaffMixin, SuccessMessageMixin, CreateView):
    model = RegistrationKey
    template_name = 'main/admin-invite.html'
    form_class = RegistrationKeyForm
    success_url = 'invite'
    success_message = '%(creation_key)s'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context

    def form_valid(self, form):
        form.instance.key = getrandbits(128)
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            creation_key=self.object.key,
        )

class InviteDeleteView(LoginRequiredMixin, UserIsStaffMixin, DeleteView):
    template_name = 'main/admin-invite-delete.html'
    model = RegistrationKey
    success_url = '/admin/invite/list'
    allow_empty = False

class ManageUsersListView(LoginRequiredMixin, UserIsAdminMixin, ListView):
    template_name = 'main/manage_users.html'
    model = User
    context_object_name = 'user_list'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'admin'
        return context
