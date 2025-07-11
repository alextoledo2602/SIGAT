# users/urls.py
from django.conf.urls import include
from . import views
from users.views import dashboard
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
"""
    The accounts/ include will give access to all the following urls
    acocunts/login/
    accounts/logout/
    accounts/password_change/
    accounts/password_change/done
    accounts/password_reset
    accounts/password_reset/done
    accounts/reset/<uidb64>/<tolen>/ to set a new password using a passowrd link
    accounts/reset/done
"""
from django.conf.urls import handler403
from .views import csrf_failure_view
from .views import agregar_dispositivo, lista_dispositivos, mantenimiento_view

handler403 = csrf_failure_view
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    #path('dashboard/', views.dashboard, name='dashboard'),
    #path('register/', views.register, name='register'),
    path('inventario/', views.inventario_view, name='inventario'),
    path('inventario/agregar/', agregar_dispositivo, name='agregar_dispositivo'),
    path('inventario/lista/', lista_dispositivos, name='lista_dispositivos'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('reports_backups/', views.reports_backups_view, name='reports_backups'),
    path('export-report/<str:format>/', views.export_report, name='export_report'),
    path('download-backup/<int:backup_id>/', views.download_backup, name='download_backup'),
    path('restore-backup/<int:backup_id>/', views.restore_backup, name='restore_backup'),
    path('mantenimiento/', mantenimiento_view, name='mantenimiento'),
    #path('login/', CustomLoginView.as_view(), name='login'),
    #path('register/<str:token>/', views.register, name='register'),
    path('', views.home_page, name = 'home_page'),
    path('push-notifications/', views.push_notifications_view, name='push_notifications'),
    path('save-token/', views.save_token, name='save_token'), 
    path("profile/", views.profile_view, name="profile"),
    path("send-profile-visit-notification", views.send_profile_visit_notification, name="send-profile-visit-notification"),
    path('send-login-notification/', views.send_login_notification, name='send_login_notification'),
      
]