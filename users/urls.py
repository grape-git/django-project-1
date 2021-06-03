from django.urls import path
from users import views

# app_name = 'register'

urlpatterns = [
    path('register/', views.register, name='register'),
]