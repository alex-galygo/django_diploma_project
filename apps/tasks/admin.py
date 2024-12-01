from django.contrib import admin

# Register your models here.

from .models import Task, FavoriteTask

admin.site.register(Task)
