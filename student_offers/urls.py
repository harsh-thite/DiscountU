# urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.discount_list, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    # Category listing and detail pages
    path('category/', views.category_list, name='category_listing'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    path('discounts/', views.discount_list, name='discount_list'),
    path('discount/<slug:slug>/', views.discount_detail, name='discount_detail'),  # Changed to <slug:slug>
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.user_profile, name='profile'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
