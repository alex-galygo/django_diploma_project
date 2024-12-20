# Generated by Django 5.1.3 on 2024-11-23 08:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('due_date', models.DateTimeField(verbose_name='Срок выполнения')),
                ('priority', models.CharField(choices=[('LOW', 'Низкий'), ('MEDIUM', 'Средний'), ('HIGH', 'Высокий')], default='MEDIUM', max_length=10, verbose_name='Приоритет')),
                ('status', models.CharField(choices=[('NEW', 'Новая'), ('IN_PROGRESS', 'В работе'), ('DONE', 'Выполнена')], default='NEW', max_length=11, verbose_name='Статус')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='FavoriteTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_tasks', to='tasks.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Избранная задача',
                'verbose_name_plural': 'Избранные задачи',
                'unique_together': {('user', 'task')},
            },
        ),
    ]
