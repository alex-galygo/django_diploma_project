from django.urls import path, include
from . import views

urlpatterns = [
    path('create/', views.create_task, name='create_task'),

    path('', views.task_list, name='index'),

]
