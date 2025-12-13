"""
企业服务URL配置
"""
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_company, name='create_company'),
    path('<str:company_id>/', views.get_company, name='get_company'),
    path('', views.list_companies, name='list_companies'),
    path('user/<str:user_id>/', views.get_user_companies, name='get_user_companies'),
    path('<str:company_id>/update/', views.update_company, name='update_company'),
    path('<str:company_id>/set_owner/', views.set_company_owner, name='set_company_owner'),
    path('<str:company_id>/join/', views.join_company, name='join_company'),
    path('<str:company_id>/leave/', views.leave_company, name='leave_company'),
    path('<str:company_id>/delete/', views.delete_company, name='delete_company'),
]
