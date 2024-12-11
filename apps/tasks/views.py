from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Task, FavoriteTask
from .forms import TaskForm


class BaseTaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user, status=self.status)

        search_query = self.request.GET.get('search', '').strip()
        if search_query:
            query = Q()
            for term in search_query.split():
                query |= Q(title__icontains=term) | Q(description__icontains=term)
            queryset = queryset.filter(query)

        sort_param = self.request.GET.get('sort')
        if sort_param:
            queryset = queryset.order_by('-priority' if sort_param == 'priority' else sort_param)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search_query': self.request.GET.get('search', ''),
            'sort': self.request.GET.get('sort', ''),
            'now': timezone.now(),
            'title': self.title,
        })
        return context


class TaskListView(BaseTaskListView):
    status = 'ACTIVЕ'
    title = 'Активные задачи'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return render(request, 'index.html')


class TaskCompleteListView(LoginRequiredMixin, BaseTaskListView):
    status = 'DONE'
    title = 'Выполненные задачи'


class FavoriteTaskListView(BaseTaskListView):
    title = 'Избранные задачи'

    def get_queryset(self):
        favorite_task_ids = FavoriteTask.objects.filter(
            user=self.request.user
        ).values_list('task_id', flat=True)
        queryset = Task.objects.filter(id__in=favorite_task_ids)
        return queryset


class AddTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для просмотра этой задачи")
        return redirect('index')


class TaskEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_edit.html'

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для редактирования этой задачи")
        return redirect('index')


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для удаления этой задачи")
        return redirect('index')


class TaskCompleteView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Task
    template_name = 'task_complete.html'

    def test_func(self):
        return self.get_object().user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для выполнения этой задачи")
        return redirect('index')

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = 'DONE'
        task.save()
        return redirect('index')


@login_required
def add_to_favorite(request, task_id):
    if request.method == 'POST':
        favorite = FavoriteTask.objects.filter(
            user=request.user,
            task_id=task_id
        )

        if favorite.exists():
            favorite.delete()
            Task.objects.filter(id=task_id).update(is_favorite=False)

            messages.success(request, 'Задача удалена из избранного')
        else:
            FavoriteTask.objects.create(
                user=request.user,
                task_id=task_id
            )
            Task.objects.filter(id=task_id).update(is_favorite=True)
            messages.success(request, 'Задача добавлена в избранное')

    return redirect(request.META.get('HTTP_REFERER', 'task_list'))

# class TaskListView(ListView, SortMixin):
#     model = Task
#     template_name = 'task_list.html'
#     context_object_name = 'tasks'
#
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return super().get(request, *args, **kwargs)
#         return render(request, 'index.html')
#
#     def get_queryset(self):
#         queryset = Task.objects.filter(user=self.request.user, status='ACTIVЕ')
#
#         search_query = self.request.GET.get('search', '').strip()
#         if search_query:
#             query = Q()
#             for term in search_query.split():
#                 query |= Q(title__icontains=term) | Q(description__icontains=term)
#             queryset = queryset.filter(query)
#
#         sort_param = self.request.GET.get('sort')
#         if sort_param:
#             queryset = queryset.order_by('-priority' if sort_param == 'priority' else sort_param)
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'search_query': self.request.GET.get('search', ''),
#             'sort': self.request.GET.get('sort', ''),
#             'now': timezone.now(),
#         })
#         return context

# class TaskCompleteListView(LoginRequiredMixin, ListView, SortMixin):
#     model = Task
#     template_name = 'task_list.html'
#     context_object_name = 'tasks'
#
#     def get_queryset(self):
#         queryset = Task.objects.filter(user=self.request.user, status='DONE')
#
#         # Поиск
#         search_query = self.request.GET.get('search', '').strip()
#         if search_query:
#             # Разбиваем поисковый запрос на отдельные слова
#             search_terms = search_query.split()
#             query = Q()
#             for term in search_terms:
#                 # Для каждого слова создаем условие поиска
#                 query |= Q(title__icontains=term) | Q(description__icontains=term)
#             queryset = queryset.filter(query)
#
#         # Сортировка
#         sort_param = self.request.GET.get('sort')
#         if sort_param:
#             queryset = queryset.order_by(sort_param)
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'search_query': self.request.GET.get('search', ''),
#             'sort': self.request.GET.get('sort', ''),
#             'now': timezone.now(),
#         })
#         return context


# class FavoriteTaskListView(LoginRequiredMixin, ListView):
#     model = Task
#     template_name = 'task_list.html'
#     context_object_name = 'tasks'
#
#     def get_queryset(self):
#         # Получаем ID задач, которые в избранном у пользователя
#         favorite_task_ids = FavoriteTask.objects.filter(
#             user=self.request.user
#         ).values_list('task_id', flat=True)
#
#         # Получаем сами задачи
#         queryset = Task.objects.filter(id__in=favorite_task_ids)
#
#         # Поиск
#         search_query = self.request.GET.get('search', '').strip()
#         if search_query:
#             search_terms = search_query.split()
#             query = Q()
#             for term in search_terms:
#                 query |= Q(title__icontains=term) | Q(description__icontains=term)
#             queryset = queryset.filter(query)
#
#         # Сортировка
#         sort_param = self.request.GET.get('sort')
#         if sort_param:
#             queryset = queryset.order_by(sort_param)
#
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'search_query': self.request.GET.get('search', ''),
#             'sort': self.request.GET.get('sort', ''),
#             'now': timezone.now(),
#             'title': 'Избранные задачи',
#         })
#         return context
