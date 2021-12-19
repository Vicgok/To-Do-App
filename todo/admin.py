from todo.models import Task
from django.contrib import admin
from django.contrib.admin.sites import site
from .models import Task
# Register your models here.
admin.site.register(Task)