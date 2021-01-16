from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from .models import User
from .models import RegistrationKey

from users.utils.position_manager import get_position_list_choices


class UserRegisterForm(UserCreationForm):
    helper = FormHelper()
    helper.form_show_labels = False
    key = forms.Field(required=True, widget=forms.TextInput(attrs={'placeholder': 'Key'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']

class UserUpdateForm(forms.ModelForm):
    CHOICES = get_position_list_choices();
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    position = forms.ChoiceField(widget=forms.Select(attrs={'disabled':'disabled'}), choices=CHOICES)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'position']


class UserAdminUpdateForm(forms.ModelForm):
    CHOICES = get_position_list_choices()
    position = forms.ChoiceField(widget=forms.Select, choices=CHOICES, label="Position")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'position', 'senior', 'staff', 'admin']

class RegistrationKeyForm(forms.ModelForm):
    CHOICES = get_position_list_choices()
    position = forms.ChoiceField(widget=forms.Select, choices=CHOICES, label="Position")
    class Meta:
        model = RegistrationKey
        fields = ['first_name', 'last_name', 'position']
