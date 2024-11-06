from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.discount_list, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('discounts/', views.discount_list, name='discount_list'),
    path('category/', views.category_list, name='category_listing'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.user_profile, name='profile'),
]