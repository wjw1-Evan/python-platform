"""
用户URL配置
"""
from django.urls import path
from apps.users import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('join-company/', views.join_company, name='join-company'),
    path('switch-company/', views.switch_company, name='switch-company'),
]
