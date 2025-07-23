from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
from . import models, views
import logging

@receiver(post_save, sender=models.User)
def create_profile_handler(sender, instance, created, **kwargs):
    if not created:
        return
    """ Create a profile and save it """
    profile = models.Profile(user=instance)
    profile.save()

from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

@receiver(post_migrate)
def setup_groups(sender, **kwargs):
    if sender.name == 'users':  # Solo para la app 'users'
        User = sender.get_model('User')
        content_type = ContentType.objects.get_for_model(User)
        ADMIN_PERMISSIONS = [
            'add_user', 'change_user', 'delete_user',
            'view_user', 'add_group', 'change_group'
        ]
        
        # Crear grupos si no existen
        admin_group, _ = Group.objects.get_or_create(name='Administradores')
        superadmin_group, _ = Group.objects.get_or_create(name='Superadministradores')
        
        # Asignar permisos
        all_permissions = Permission.objects.filter(content_type=content_type, codename__in=ADMIN_PERMISSIONS)
        superadmin_group.permissions.set(all_permissions)
        admin_group.permissions.set(all_permissions.exclude(codename__contains='delete'))

#LOGGIN PARA LA CONSOLA PARA VERIFICAR QUE LOS USUARIOS ESTAN INCIANDO SESION CORRECTAMENTE
logger = logging.getLogger(__name__)
@receiver(user_logged_in)
def log_user_login (sender, request, user, **kwargs):
    ip = request.META.get("REMOTE_ADDR", "IP-no-disponible")
    logger.info(f"Usuario {user.username} ha iniciado sesion. IP: {ip}")


#Creacion de registros relacionados
from django.utils import timezone

@receiver(post_save, sender=models.DispositivoInventario)
def crear_registros_relacionados(sender, instance, created, **kwargs):
    if created and instance.creado_por:
        # 1. Crear un reporte inicial de inventario
        models.Reporte.objects.create(
            tipo_reporte='inventario',
            titulo=f"Nuevo dispositivo {instance.numero_inventario}",
            contenido={
                'numero_inventario': instance.numero_inventario,
                'tipo': instance.tipo,
                'marca': instance.marca,
                'modelo': instance.modelo,
                'accion': 'creacion'
            },
            generado_por=instance.creado_por
        )
        
        # 2. Crear un mantenimiento preventivo inicial
        mantenimiento = models.Mantenimiento.objects.create(
            tipo='preventivo',
            estado='programado',
            descripcion=f"Mantenimiento inicial para dispositivo {instance.numero_inventario}",
            realizado_por=instance.creado_por,
            fecha_programada=timezone.now() + timezone.timedelta(days=30)
        )
        
        # 3. Asociar el dispositivo al mantenimiento
        mantenimiento.dispositivo = instance
        mantenimiento.save()
        
        # 4. Opcional: Asignar al usuario que lo creó si es necesario
        if instance.creado_por:
            # Actualización directa del campo responsable (evitando bucle con update)
            models.DispositivoInventario.objects.filter(pk=instance.pk).update(
                responsable=instance.creado_por
            )
            
            # Opcional: Si se necesita registrar este cambio en Reporte
            models.Reporte.objects.create(
                tipo_reporte='asignacion',
                titulo=f"Asignación inicial dispositivo {instance.numero_inventario}",
                contenido={
                    'numero_inventario': instance.numero_inventario,
                    'responsable': str(instance.creado_por),
                    'accion': 'asignacion_inicial'
                },
                generado_por=instance.creado_por
            )