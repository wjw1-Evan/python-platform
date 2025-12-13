"""
用户服务URL配置
"""
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_user, name='create_user'),
    path('login/', views.login, name='login'),
    path('<str:user_id>/', views.get_user, name='get_user'),
    path('', views.list_users, name='list_users'),
    path('<str:user_id>/update/', views.update_user, name='update_user'),
    path('<str:user_id>/update_company_id/', views.update_user_company_id, name='update_user_company_id'),
    path('<str:user_id>/delete/', views.delete_user, name='delete_user'),
]
