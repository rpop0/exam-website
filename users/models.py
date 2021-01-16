from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    position = models.IntegerField(default=0)
    email = models.EmailField()
    senior = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse('users-settings', kwargs={'pk': self.pk})

class RegistrationKey(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    position = models.IntegerField(default=0)
    email = models.EmailField()
    key = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.key}'
