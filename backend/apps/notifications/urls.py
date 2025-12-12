"""
通知URL配置
"""
from django.urls import path
from apps.notifications import views

urlpatterns = [
    path('', views.list_notifications, name='list-notifications'),
    path('create/', views.create_notification, name='create-notification'),
    path('unread-count/', views.unread_count, name='unread-count'),
    path('mark-all-read/', views.mark_all_as_read, name='mark-all-read'),
    path('<str:notification_id>/', views.get_notification, name='get-notification'),
    path('<str:notification_id>/read/', views.mark_as_read, name='mark-as-read'),
    path('<str:notification_id>/delete/', views.delete_notification, name='delete-notification'),
]
