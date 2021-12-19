from django.urls import path
from . import views

#app_name = 'todo'

urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerPage, name="register"),
    path("my-account/", views.myAccount, name="my-account"),


    path("", views.taskList, name="tasks"),
    path("task/<int:pk>/", views.taskDetail, name="task-detail"),
    path("task-create/", views.taskCreate, name="task-create"),
    path("task-update/<int:pk>", views.taskUpdate, name="task-update"),
    path("task-delete/<int:pk>", views.taskDelete, name="task-delete"),

    ]
