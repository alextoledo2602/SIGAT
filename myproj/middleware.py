from django.http import JsonResponse
import json
from django.conf import settings

class APIResponseMiddleware:
    """
    Middleware que asegura respuestas JSON consistentes para endpoints de API
    y maneja errores apropiadamente.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.api_prefixes = getattr(settings, 'API_PREFIXES', ['/api/', '/auth/'])
        self.json_endpoints = getattr(settings, 'JSON_ENDPOINTS', [
            '/check-fcm-token/',
            '/send-login-notification/'
        ])

    def __call__(self, request):
        response = self.get_response(request)
        
        # Verificar si es una ruta API
        is_api_path = any(
            request.path.startswith(prefix) 
            for prefix in self.api_prefixes
        ) or request.path in self.json_endpoints
        
        if is_api_path:
            # Manejar errores 500
            if response.status_code == 500:
                return JsonResponse({
                    'status': 'error',
                    'code': 'server_error',
                    'message': 'Internal server error'
                }, status=500)
            
            # Manejar errores 404
            if response.status_code == 404:
                return JsonResponse({
                    'status': 'error',
                    'code': 'not_found',
                    'message': 'Endpoint not found'
                }, status=404)
            
            # Convertir respuestas no-JSON inesperadas
            if not self.is_json_response(response):
                try:
                    content = response.content.decode('utf-8')
                    return JsonResponse({
                        'status': 'error',
                        'code': 'invalid_response',
                        'message': 'Unexpected response format',
                        'original_content': content[:200]  # Solo primeros 200 caracteres
                    }, status=response.status_code)
                except:
                    return JsonResponse({
                        'status': 'error',
                        'code': 'invalid_response',
                        'message': 'Could not parse server response'
                    }, status=response.status_code)
        
        return response

    def is_json_response(self, response):
        """Verifica si la respuesta es JSON válido"""
        if hasattr(response, 'is_json') and response.is_json:
            return True
        content_type = response.get('Content-Type', '')
        return 'application/json' in content_type