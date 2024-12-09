from django.urls import path, include
from . import views
from .views import AddTask, TaskEditView, TaskDeleteView, TaskView, TaskListView, TaskCompleteView, FavoriteTaskListView, TaskCompleteListView

urlpatterns = [
    path('create/', AddTask.as_view(), name='create_task'),

    path('', TaskListView.as_view(), name='index'),

    path('task/<int:pk>/', TaskView.as_view(), name='task_detail'),

    path('task/<int:pk>/edit/', TaskEditView.as_view(), name='task_edit'),

    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

    # path('task/<int:pk>/favorite/', views.favorite_task, name='favorite_task'),

    path('task/<int:pk>/completed/', TaskCompleteView.as_view(), name='task_complete'),

    path('task/favorite/', FavoriteTaskListView.as_view(), name='task_favorite'),

    path('task/add_to_favorite/<int:task_id>/', views.add_to_favorite, name='add_to_favorite'),

    path('task/complite/', TaskCompleteListView.as_view(), name='task_list_complete'),

]
