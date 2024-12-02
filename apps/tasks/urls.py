from django.urls import path, include
from . import views
from .views import AddTask, TaskEditView, TaskDeleteView, TaskView, TaskListView

urlpatterns = [
    path('create/', AddTask.as_view(), name='create_task'),

    path('', views.TaskListView.as_view(), name='index'),

    path('task/<int:pk>/', TaskView.as_view(), name='task_detail'),

    path('task/<int:pk>/edit/', TaskEditView.as_view(), name='task_edit'),

    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

]
