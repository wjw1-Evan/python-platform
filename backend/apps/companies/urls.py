"""
企业URL配置
"""
from django.urls import path
from apps.companies import views

urlpatterns = [
    path('', views.list_companies, name='list-companies'),
    path('create/', views.create_company, name='create-company'),
    path('<str:company_id>/', views.get_company, name='get-company'),
    path('<str:company_id>/update/', views.update_company, name='update-company'),
    path('<str:company_id>/delete/', views.delete_company, name='delete-company'),
    path('<str:company_id>/members/', views.get_members, name='get-members'),
    path('<str:company_id>/remove-member/', views.remove_member, name='remove-member'),
]
