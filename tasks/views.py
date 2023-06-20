from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from django.utils import timezone

# Create your views here.

# Public Views (Every user that visit the web app can access this views)
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })

    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,
                     username=request.POST['username'],
                     password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error' : 'Username or Password is incorrect'
        })
        else:
            login(request, user)
            return redirect('tasks')

# Protected Views (Only authenticated users can access to this views)
@login_required
def tasks(request):
    tasks = Task.objects.filter(
        user=request.user,
        datecompleted__isnull=True
        )
    return render(request, 'tasks.html', {'tasks' : tasks, "status": "Pending"})

@login_required
def taskDetail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk = task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task' : task, 'form' : form} )
    else:
        try: 
            task = get_object_or_404(Task, pk = task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task' : task, 
                'form' : form,
                'error' : "Error Updating Task"
                })

@login_required
def completeTask(request, task_id):
    task = get_object_or_404(Task, pk= task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required 
def deleteTask(request, task_id):
    task = get_object_or_404(Task, pk= task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def tasksCompleted(request):
    tasks = Task.objects.filter(
        user=request.user,
        datecompleted__isnull=False
        ).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks' : tasks, "status": "Completed"})

@login_required
def createTask(request):
    if (request.method == 'GET'):
        return render(request, 'createTask.html', {
        'form' : TaskForm
    })
    else: 
        try:
            
            form = TaskForm(request.POST)
            print(form)
            new_task = form.save(commit=False);
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
            
        except ValueError:
            return render(request, 'createTask.html', {
                'form' : TaskForm,
                'error' : "Please provide valid data"
            })

@login_required
def signout(request):
    logout(request)
    return redirect('home')



