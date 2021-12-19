from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from django.forms import ModelForm
from django.http import HttpResponse,request

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['user']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    

        


    

        



