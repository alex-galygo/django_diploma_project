from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1, 'Низкий'
        MEDIUM = 2, 'Средний'
        HIGH = 3, 'Высокий'

    STATUS_CHOICES = [
        ('ACTIVЕ', 'Активна'),
        ('DONE', 'Выполнена'),

    ]

    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='tasks',
                             verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    due_date = models.DateField(verbose_name='Дата выполнения', blank=True, null=True)
    priority = models.IntegerField(choices=Priority.choices,
                                   default=Priority.MEDIUM,
                                   verbose_name='Приоритет')
    status = models.CharField(max_length=11,
                              choices=STATUS_CHOICES,
                              default='ACTIVЕ',
                              verbose_name='Статус')

    is_favorite = models.BooleanField(default=False, verbose_name='В избранном')

    class Meta:
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи'
        ordering = ['due_date']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['priority']),
            models.Index(fields=['due_date']),
            models.Index(fields=['is_favorite']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'pk': self.pk})


class FavoriteTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_tasks',
                             verbose_name='Пользователь')
    task = models.ForeignKey(Task, on_delete=models.CASCADE,
                             related_name='favorite_tasks',
                             verbose_name='Задача')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Избранную задачу'
        verbose_name_plural = 'Избранные задачи'
        unique_together = ['user', 'task']

    def __str__(self):
        return f'{self.user} - {self.task}'


# from django.db import models
# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from django.utils.translation import gettext_lazy as _
# from django.core.validators import MinValueValidator, MaxValueValidator
#
# User = get_user_model()
#
#
# class TaskManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().select_related('user')
#
#     def active(self):
#         return self.get_queryset().filter(status='ACTIVE')
#
#     def favorites(self, user):
#         return self.get_queryset().filter(user=user, is_favorite=True)
#
#
# class Task(models.Model):
#     class Priority(models.IntegerChoices):
#         LOW = 1, _('Низкий')
#         MEDIUM = 2, _('Средний')
#         HIGH = 3, _('Высокий')
#
#     class Status(models.TextChoices):
#         ACTIVE = 'ACTIVE', _('Активна')
#         DONE = 'DONE', _('Выполнена')
#
#     title = models.CharField(
#         max_length=100,
#         verbose_name=_('Заголовок'),
#         db_index=True  # Индекс для частых поисков по заголовку
#     )
#     description = models.TextField(
#         verbose_name=_('Описание'),
#         blank=True,
#         default=''  # Явное значение по умолчанию вместо NULL
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='tasks',
#         verbose_name=_('Пользователь'),
#         db_index=True
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name=_('Дата создания'),
#         db_index=True
#     )
#     due_date = models.DateField(
#         verbose_name=_('Дата выполнения'),
#         blank=True,
#         null=True,
#         db_index=True
#     )
#     priority = models.PositiveSmallIntegerField(
#         choices=Priority.choices,
#         default=Priority.MEDIUM,
#         verbose_name=_('Приоритет'),
#         validators=[MinValueValidator(1), MaxValueValidator(3)],
#         db_index=True
#     )
#     status = models.CharField(
#         max_length=6,  # Уменьшен размер поля, так как максимальная длина 'ACTIVE'
#         choices=Status.choices,
#         default=Status.ACTIVE,
#         verbose_name=_('Статус'),
#         db_index=True
#     )
#     is_favorite = models.BooleanField(
#         default=False,
#         verbose_name=_('В избранном'),
#         db_index=True
#     )
#
#     objects = TaskManager()
#
#     class Meta:
#         verbose_name = _('Задачу')
#         verbose_name_plural = _('Задачи')
#         ordering = ['-created_at']
#         indexes = [
#             models.Index(fields=['user', 'status']),  # Составной индекс для частых запросов
#             models.Index(fields=['user', 'is_favorite']),
#             models.Index(fields=['user', 'due_date']),
#         ]
#         constraints = [
#             models.CheckConstraint(
#                 check=models.Q(priority__in=[1, 2, 3]),
#                 name='valid_priority'
#             )
#         ]
#
#     def __str__(self):
#         return f"{self.title} ({self.get_status_display()})"
#
#     def get_absolute_url(self):
#         return reverse('task_detail', kwargs={'pk': self.pk})
#
#     @property
#     def is_overdue(self):
#         from django.utils import timezone
#         return bool(self.due_date and self.due_date < timezone.now().date())
#
#     def save(self, *args, **kwargs):
#         # Если задача выполнена, убираем её из избранного
#         if self.status == self.Status.DONE:
#             self.is_favorite = False
#         super().save(*args, **kwargs)
#
#
# class FavoriteTask(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='favorite_tasks',
#         verbose_name=_('Пользователь')
#     )
#     task = models.ForeignKey(
#         Task,
#         on_delete=models.CASCADE,
#         related_name='favorite_tasks',
#         verbose_name=_('Задача')
#     )
#     added_at = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name=_('Дата добавления')
#     )
#
#     class Meta:
#         verbose_name = _('Избранную задачу')
#         verbose_name_plural = _('Избранные задачи')
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'task'],
#                 name='unique_user_task_favorite'
#             )
#         ]
#         indexes = [
#             models.Index(fields=['user', 'added_at']),
#         ]
#
#     def __str__(self):
#         return f"{self.user.username} - {self.task.title}"
#
#     def save(self, *args, **kwargs):
#         if not self.pk:  # Если объект создаётся впервые
#             self.task.is_favorite = True
#             self.task.save(update_fields=['is_favorite'])
#         super().save(*args, **kwargs)
#
#     def delete(self, *args, **kwargs):
#         self.task.is_favorite = False
#         self.task.save(update_fields=['is_favorite'])
#         super().delete(*args, **kwargs)
