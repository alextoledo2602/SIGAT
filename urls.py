from django.urls import path
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from users.views import (
    get_csrf,
    CustomLoginAPIView,
    DashboardDataAPIView,
    UserProfileAPIView,
    DispositivoInventarioViewSet,  
    ReportsBackupsViewSet,
    ExportReportAPIView,
    BackupOperationsAPIView,
    MantenimientoViewSet,
    PushNotificationAPIView,
    FCMTokenAPIView,
    ProfileAPIView,
    HomeAPIView,
    UserViewSet
)

router = DefaultRouter()
router.register(r'api/mantenimientos', MantenimientoViewSet, basename='mantenimiento')
router.register(r'api/users', UserViewSet, basename='users')
router.register(r'api/dispositivos', DispositivoInventarioViewSet, basename='dispositivos')
router.register(r'api/reportes-backups', ReportsBackupsViewSet, basename='reportes-backups')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', CustomLoginAPIView.as_view(), name='api-login'),  # Añade .as_view()
    path('api/auth/csrf/', get_csrf, name='get_csrf'),
    path('api/home/', HomeAPIView.as_view(), name='api-home'),  # Añade .as_view()
    path('api/dashboard/', DashboardDataAPIView.as_view(), name='api-dashboard'),  # Añade .as_view()
    path('api/profile/', ProfileAPIView.as_view(), name='api-profile'),  # Añade .as_view()
    path('api/export/<str:format>/', ExportReportAPIView.as_view(), name='api-export'),  # Añade .as_view()
    path('api/backups/<int:backup_id>/', BackupOperationsAPIView.as_view(), name='api-backup-operations'),  # Añade .as_view()
    path('api/notifications/', PushNotificationAPIView.as_view(), name='api-notifications'),  # Añade .as_view()
    path('api/fcm-token/', FCMTokenAPIView.as_view(), name='api-fcm-token'),  # Añade .as_view()
] + router.urls