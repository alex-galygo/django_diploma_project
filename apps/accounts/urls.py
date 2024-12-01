from django.urls import path, include
from . import views
from .views import UserRegistration

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),

    path('login/', views.CustomLoginView.as_view(redirect_authenticated_user=True), name='login'),
]
