"""
URL configuration for admin platform project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/companies/', include('apps.companies.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
    path('api/logs/', include('apps.logs.urls')),
]
