from django.contrib import admin
from .models import RegistrationKey, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'position')

@admin.register(RegistrationKey)
class RegistrationKeyAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'key', 'position')
