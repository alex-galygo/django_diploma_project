from rest_framework import generics, viewsets
from ..tasks.models import Task, FavoriteTask
from .serializers import TaskSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


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
