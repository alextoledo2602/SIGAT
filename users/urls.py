# users/urls.py
from django.conf.urls import include
from . import views
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
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    csrf_failure_view,
    CustomLoginView,
    custom_logout,
    push_notifications_view,
    get_csrf,
    profile_view,
    save_token,
    get_token,
    send_profile_visit_notification
)

handler403 = csrf_failure_view

urlpatterns = [
    # Rutas de autenticación y páginas tradicionales
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/auth/csrf/', get_csrf, name='get_csrf'),
    path('profile/', profile_view, name="profile"),
    path('push-notifications/', push_notifications_view, name='push_notifications'),
    path('save-token/', save_token, name='save_token'),
    path('send-profile-visit-notification/', send_profile_visit_notification, name='send-profile-visit-notification'),
]