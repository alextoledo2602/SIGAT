# myproj/middleware/__init__.py

"""
Package que contiene todos los middlewares personalizados del proyecto.

Los middlewares deben ser importados aquí para facilitar su acceso desde settings.py
"""

# Importa aquí tus middlewares personalizados para exponerlos directamente desde el paquete
from .custom_cors import CustomCorsMiddleware
from .csrf_handler import CustomCsrfMiddleware
from .security import SecurityHeadersMiddleware

# Opcional: Exporta los middlewares para poder importarlos directamente desde el paquete
__all__ = [
    'CustomCorsMiddleware',
    'CustomCsrfMiddleware',
    'SecurityHeadersMiddleware',
]