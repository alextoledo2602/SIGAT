from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

class GuestRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Solo aplicar si el usuario está autenticado y es invitado
        if request.user.is_authenticated and request.user.role == 'invitado':
            allowed_paths = [
                '/api/home/',  # Ajusta según tus URLs reales
                '/api/reportes/',
                '/dashboard/',  # Home del dashboard
                '/dashboard/reportes'  # Ruta de reportes
            ]
            
            # Verificar si la ruta actual no está permitida
            if not any(request.path.startswith(path) for path in allowed_paths):
                return JsonResponse(
                    {'error': 'Acceso restringido para usuarios invitados'},
                    status=403
                )