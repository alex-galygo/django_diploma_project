from rest_framework import generics, viewsets
from ..tasks.models import Task, FavoriteTask
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


# class TaskAPIView(generics.ListCreateAPIView):
#     serializer_class = TaskSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'description']
#     ordering_fields = ['created_at', 'due_date', 'priority']
#
#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)
#
#
# class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = TaskSerializer
#
#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_to_favorite(self, request, pk=None):
        task = self.get_object()
        favorite, created = FavoriteTask.objects.get_or_create(user=request.user, task=task)
        if not created:
            favorite.delete()
            task.is_favorite = False
            task.save()
            return Response({'status': 'Задача удалена из избранного'}, status=status.HTTP_200_OK)
        task.is_favorite = True
        task.save()
        return Response({'status': 'Задача добавлена в избранное'}, status=status.HTTP_200_OK)


class FavoriteTaskViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        favorite_task_ids = FavoriteTask.objects.filter(user=self.request.user).values_list('task_id', flat=True)
        return Task.objects.filter(id__in=favorite_task_ids)
