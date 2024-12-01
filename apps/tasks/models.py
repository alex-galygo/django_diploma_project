from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Низкий'),
        ('MEDIUM', 'Средний'),
        ('HIGH', 'Высокий'),
    ]

    STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('IN_PROGRESS', 'В работе'),
        ('DONE', 'Выполнена'),
    ]

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='tasks',
                             verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    due_date = models.DateTimeField(verbose_name='Срок выполнения', blank=True, null=True)
    priority = models.CharField(max_length=10,
                                choices=PRIORITY_CHOICES,
                                default='MEDIUM',
                                verbose_name='Приоритет')
    status = models.CharField(max_length=11,
                              choices=STATUS_CHOICES,
                              default='NEW',
                              verbose_name='Статус')

    class Meta:
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class FavoriteTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_tasks',
                             verbose_name='Пользователь')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='favorite_tasks',
                             verbose_name='Задача')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Избранная задача'
        verbose_name_plural = 'Избранные задачи'
        unique_together = ['user', 'task']

    def __str__(self):
        return f'{self.user} - {self.task}'
