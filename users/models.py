from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from pywebpush import WebPushException, webpush
import json

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier for 
    authentication instead of username.
    Between the username field (email) and password, you must put all
    the required fields. extra_fields must contain all the optional 
    fields.
    """
    
    def create_user(self, id, email, username, password, role="invitado", **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_("Users must have a Username"))
        if not id:
            raise ValueError(_("Users must have an ID"))
        user = self.model(
        id=id,
        email=self.normalize_email(email),
        username=username,
        role=role,
        **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
    
        # Asignar grupo según el rol
        from django.contrib.auth.models import Group
        if role == 'superadmin':
            group = Group.objects.using(self._db).get(name='Superadministradores')
            user.groups.add(group)
            user.is_staff = True
            user.is_superuser = True
        elif role == 'admin':
            group = Group.objects.using(self._db).get(name='Administradores')
            user.groups.add(group)
            user.is_staff = True
        user.save(using=self._db)  # Asegurar uso de la DB correcta
        user.sync_role_to_group(using=self._db)  # Sincronizar después de guardar
        return user
        
   
    
    def create_superuser(self, id, email, username, password):
        user = self.create_user(
            id=id,
            email=email,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

"""
This model behaves identically to the default user model, but you’ll be able to customize it in the future if the need arises. This is the recommended behavior
"""

class User(AbstractUser):
    class Meta:
        db_table = 'users'
    ROLES = (("superadmin", "Super Admin"), ("admin", "Admin"), ("invitado", "Invitado"))
    role = models.CharField(max_length=20, choices=ROLES, default="invitado")
    email = models.EmailField(_('email address'), unique=True)
    id = models.CharField(max_length=11, primary_key=True)
    USERNAME_FIELD = 'username'

    """
    The REQUIRED_FIELDS = ['username'] must be present, otherwise the following error will arise:
        TypeError: create_superuser() missing 1 required positional argument: 'username'
    """
    REQUIRED_FIELDS = ['id', 'email']
    objects = CustomUserManager()

    def getEmailField(self):
        return self.email

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def sync_role_to_group(self, using='default'):
        """Sincroniza el rol con grupos usando la base de datos correcta"""
        from django.contrib.auth.models import Group
    
    # Usar la misma DB que el usuario
        Group = Group.objects.using(using)
    
        self.groups.clear()
    
        if self.role == 'superadmin':
            group, _ = Group.get_or_create(name='Superadministradores')
            self.groups.add(group)
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'admin':
            group, _ = Group.get_or_create(name='Administradores')
            self.groups.add(group)
            self.is_staff = True
            self.is_superuser = False






    def send_login_notification(self):
        from django.utils import timezone
        login_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        message = {
            "title": "Nuevo inicio de sesión",
            "body": f"El usuario {self.username} inició sesión el {login_time}",
            "icon": "/static/images/icon.png"
        }
        
        # Enviar a dispositivos FCM
        if hasattr(self, 'fcmtoken') and self.fcmtoken.is_active:
            from pyfcm import FCMNotification
            push_service = FCMNotification(api_key=settings.FCM_API_KEY)
            push_service.notify_single_device(
                registration_id=self.fcmtoken.token,
                message_title=message["title"],
                message_body=message["body"]
            )
        
        # Enviar a dispositivos web push
        devices = self.devices_set.all()
        for device in devices:
            try:
                webpush(
                    subscription_info={
                        "endpoint": device.endpoint,
                        "keys": {
                            "p256dh": device.p256dh,
                            "auth": device.auth
                        }
                    },
                    data=json.dumps(message),
                    vapid_private_key=settings.VAPID_PRIVATE_KEY,
                    vapid_claims={
                        "sub": f"mailto:{settings.FIREBASE_SECRETS.get('user_email', 'default@example.com')}"
                    }
                )
            except WebPushException as ex:
                print("Error al enviar notificación:", ex)

class DispositivoInventario(models.Model):
    TIPO_CHOICES = [
        ('computadora', 'Computadora'),
        ('movil', 'Móvil'),
        ('telefono_fijo', 'Teléfono Fijo'),
        ('impresora', 'Impresora'),
        ('router', 'Router'),
        ('switcher', 'Switcher'),
        ('otro', 'Otro'),
    ]
    
    MARCA_CHOICES = [
        ('Dell', 'Dell'),
        ('HP', 'HP'),
        ('Lenovo', 'Lenovo'),
        ('Apple', 'Apple'),
        ('Asus', 'Asus'),
        ('Acer', 'Acer'),
        ('Otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('En reparación', 'En reparación'),
        ('Baja', 'Baja'),
    ]
    
    UBICACION_CHOICES = [
        ('Departamento de Sistema', 'Departamento de Sistema'),
        ('Gerencia Financiera', 'Gerencia Financiera'),
        ('Seguridad y Proteccion', 'Seguridad y Protección'),
        ('Atención al hombre', 'Atención al hombre'),
        ('Auditoria', 'Auditoría'),
    ]

    numero_inventario = models.CharField(max_length=50, unique=True, primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=20, choices=MARCA_CHOICES)
    modelo = models.CharField(max_length=100)
    serial = models.CharField(max_length=50, unique=True)
    ubicacion = models.CharField(max_length=50, choices=UBICACION_CHOICES)
    fecha_adquisicion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    responsable = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='dispositivos_asignados',
        verbose_name='Usuario asignado'  # usuario_id en modelo lógico
    )  
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='dispositivos_creados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dispositivos_inventario'  # Nombre de la tabla
        managed = True  # Esto permite a Django gestionar la tabla
        verbose_name = 'Dispositivo de Inventario'
        verbose_name_plural = 'Dispositivos de Inventario'

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.numero_inventario})"

class Mantenimiento(models.Model):
    TIPO_CHOICES = (
        ('preventivo', 'Preventivo'),
        ('correctivo', 'Correctivo'),
    )
    
    ESTADO_CHOICES = (
        ('programado', 'Programado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    )
    
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='programado')
    descripcion = models.TextField()
    dispositivo = models.ForeignKey(
        DispositivoInventario, 
        on_delete=models.CASCADE,
        null=True,
        related_name='mantenimientos',
        verbose_name='Dispositivo'  # dispositivo_id en modelo lógico
    )
    realizado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='mantenimientos_realizados'
    )
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    fecha_programada = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mantenimiento'
        verbose_name = 'Mantenimiento'
        verbose_name_plural = 'Mantenimientos'

    def __str__(self):
        return f"Mantenimiento {self.tipo} - {self.estado}"


class Reporte(models.Model):
    TIPO_CHOICES = (
        ('inventario', 'Inventario'),
        ('actividad', 'Actividad'),
        ('mantenimiento', 'Mantenimiento'),
        ('incidencia', 'Incidencia'),
    )
    
    id = models.AutoField(primary_key=True)
    tipo_reporte = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=200)
    contenido = models.JSONField()  # Para almacenar datos estructurados. Campo parámetros en el modelo lógico
    generado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='reportes_generados'
    )
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    ruta_archivo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'reporte'
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

    def __str__(self):
        return f"Reporte {self.tipo_reporte} - {self.titulo}"

class Backup(models.Model):
    TIPO_CHOICES = (
        ('completo', 'Completo'),
        ('diferencial', 'Diferencial'),
        ('incremental', 'Incremental'),
    )
    
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    tamaño = models.BigIntegerField()  # En bytes
    ubicacion = models.CharField(max_length=255)
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='backups_creados'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'backup'
        verbose_name = 'Backup'
        verbose_name_plural = 'Backups'

    def __str__(self):
        return f"Backup {self.tipo} - {self.descripcion}"









class Profile(models.Model):
    class Meta:
        db_table = 'profiles'
    
    user = models.OneToOneField(User, 
        on_delete=models.CASCADE, 
        primary_key = True
    )
    birthdate = models.DateField(null=True, default=None)
    # the min length should be defined by a custom validator
    personal_ad = models.TextField(max_length=2000, blank=True)
    # sex
    # country
    # state
    # city
    # pics have a foreign key to this table. They will be the 3rd step
    # on user registration
    # must be put there in order to not to change the deafult Django user
    email_confirmed = models.BooleanField(default=False)
    # check whether the user provided the basic mandatory profile data
    is_valid_profile = models.BooleanField(default=False)
   

class FCMToken(models.Model):
    class Meta:
        db_table = 'fcm_tokens'
    
    user = models.OneToOneField(User, 
        on_delete=models.CASCADE, 
        primary_key = True
    )
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    device_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Token for {self.user.username}"
class Devices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True,
    blank=True)
    endpoint = models.URLField(max_length=500)
    p256dh = models.CharField(max_length=500)
    auth = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dispositivo de {self.user.username}"


