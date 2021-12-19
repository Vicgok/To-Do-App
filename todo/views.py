from django.contrib import auth
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Task
from .forms import TaskForm, CustomUserCreationForm
from todo import forms

import re

# Create your views here.

# view login
def loginPage(request):
    loginError = ''
    username = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            loginError = 'Login failed\ninvalid username or password'
        
    context = {
            'username':username,
            'loginError':loginError,
        }
    
    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'todo/login.html',context)

# view logout
def logoutUser(request):
    logout(request)
    return redirect('login')

# view for user registeration
def registerPage(request):
    form = CustomUserCreationForm()
    usernameError = ''
    emailError = ''
    passwordError = ''
    duplicate_username = ''
    username =''
    errorFlag = False
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST or None)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
        duplicate_username = User.objects.filter(username = username)
        duplicate_email = User.objects.filter(email = email)

        if duplicate_username:
            usernameError = 'Username already exist'
            errorFlag = True

        
        if (re.match(regex, email)):
            if duplicate_email:
                emailError = 'Email already exist'
                errorFlag = True
        else:
            emailError = 'Invalid email address'
            errorFlag = True

        if password1 != password2:
            passwordError = 'Password fields dosen\'t match'
            errorFlag = True

        if errorFlag == False:
            if form.is_valid():
                form.save()
                return redirect('login')
           
    
    context = {
            'form':form,
            'usernameError': usernameError,
            'emailError': emailError,
            'username':username,
            'passwordError':passwordError,
            'duplicate_username':duplicate_username
        }
    return render(request, 'todo/register.html',context)

# view for Account details 
@login_required(login_url='login')
def myAccount(request):
    tasks = Task.objects.filter(user = request.user)
    total_tasks = tasks.count()
    tasks_completed = tasks.filter(complete=True).count()
    tasks_incomplete = tasks.filter(complete=False).count()
    
    context={
        'total_task':total_tasks,
        'tasks_completed': tasks_completed,
        'tasks_incomplete':tasks_incomplete,
    }

    return render(request, 'todo/my_account.html',context)

# view to display tasks for logged in user
@login_required(login_url='login')
def taskList(request):
    tasks = Task.objects.filter(user=request.user)
    count = tasks.filter(complete=False).count()

    search_input = request.GET.get('search-area') or ''
    if search_input:
       tasks = tasks.filter(title__startswith=search_input)
    
    context = {
        'tasks': tasks,
        'count': count,
        'search_input': search_input,
    }

    return render(request, 'todo/task_list.html', context)

# view to display tasks details for logged in user
@login_required(login_url='login')
def taskDetail(request, pk):
    task = Task.objects.get(id=pk)
    context = {
        'task':task
    }
    return render(request, 'todo/task_detail.html',context)

# view to add a new task
@login_required(login_url='login')
def taskCreate(request):
    
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('/')
        
    context = {
            'form': form
        }

    return render(request, 'todo/task_create.html', context)

# view to update a task
@login_required(login_url='login')
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    
    form = TaskForm(instance=task)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'task':task,
        'form': form
    }

    return render(request, 'todo/task_update.html', context)

# view to delete a task
@login_required(login_url='login')
def taskDelete(request, pk):
    task = Task.objects.get(id = pk)

    if request.method == 'POST':
        task.delete()
        return redirect('/')
        
    context = {
        'task': task,
    }

    return render(request, 'todo/task_delete.html', context)


    
    