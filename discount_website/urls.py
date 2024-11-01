# urls.py in discount_website

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('student_offers.urls')),  # Include app URLs
]
