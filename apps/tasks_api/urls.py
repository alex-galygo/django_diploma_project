from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='task')
router.register(r'favorite-task', FavoriteTaskViewSet, basename='favorite-task')

urlpatterns = [

    path('api-autch', include('rest_framework.urls')),

    # path('tasklist', TaskAPIView.as_view(), name='tasklist'),
    #
    # path('task-update-delete/<int:pk>', TaskDetailAPIView.as_view(), name='task-update-delete'),

    path('', include(router.urls)),

    path("schema/", SpectacularAPIView.as_view(), name="schema"),

    path("schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui")
]
