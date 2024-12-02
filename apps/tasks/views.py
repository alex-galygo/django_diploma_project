from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .forms import TaskForm, Task


class AddTask(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'create_task.html'
    success_url = 'task_list'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return render(request, 'index.html')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


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

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})


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

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.pk})


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав для удаления этой задачи")
        return redirect('index')
