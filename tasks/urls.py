from django.urls import path
from . import views

urlpatterns = [
    # User Authentication
    path('signup/', views.signup, name="signup"),
    path('logout/', views.signout, name="logout"),
    path('signin/', views.signin, name="signin"),

    # Main Web Site Pages
    path('', views.home, name="home"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks_completed/', views.tasksCompleted, name="tasks_completed"),

    # Task Model Operations
    path('tasks/create', views.createTask, name="createTask"),
    path('tasks/<int:task_id>/', views.taskDetail, name="task_detail"),
    path('tasks/<int:task_id>/complete', views.completeTask, name="complete_task"),
    path('tasks/<int:task_id>/delete', views.deleteTask, name="delete_task")
       
]