# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.discount_list, name='discount_list'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
]
