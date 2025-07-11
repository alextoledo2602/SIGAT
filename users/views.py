from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login
from django.template import RequestContext

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views.generic import View, UpdateView
from django.utils.translation import gettext as _
from .models import User
from django.http import HttpResponse
from myproj.firebase_config import initialize_firebase
import firebase_admin
import os, json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from myproj.firebase_config import initialize_firebase
from myproj import settings

from django.http import JsonResponse # type:ignore
from django.contrib.auth.decorators import login_required # type:ignore
from pywebpush import webpush, WebPushException
import json
from datetime import datetime
from myproj import *
from django.contrib.auth.views import LoginView
from .models import FCMToken, Devices
from pyfcm import FCMNotification
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework import generics
from .serializers import UserSerializer
from django.db.models import Q
from django.utils.dateparse import parse_date
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

@method_decorator(ensure_csrf_cookie, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Asegúrate de tener este template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fuerza la generación del token CSRF si no está presente
        if 'csrf_token' not in context:
            from django.middleware.csrf import get_token
            context['csrf_token'] = get_token(self.request)
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            user = form.get_user()
            return JsonResponse({
                'success': True,
                'redirect_url': self.get_success_url(),
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            })
        return response

    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors.as_json(),
                'message': 'Invalid login credentials'
            }, status=400)
        return super().form_invalid(form)
    
    def send_login_notification(self, user):
        """Envía notificaciones push sobre el inicio de sesión"""
        login_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        message = {
            "title": "Nuevo inicio de sesión",
            "body": f"El usuario {user.username} inició sesión el {login_time}",
            "icon": "/static/images/icon.png",
            "timestamp": login_time
        }
        
        # 1. Enviar notificación FCM (para apps móviles)
        self._send_fcm_notification(user, message)
        
        # 2. Enviar notificación Web Push (para navegadores)
        self._send_web_push_notification(user, message)
    
    def send_fcm_notification(self, user, message):
        """Envía notificación a través de Firebase Cloud Messaging"""
        try:
            # Verificar si el usuario tiene un token FCM activo
            if hasattr(user, 'fcmtoken') and user.fcmtoken.is_active:
                push_service = FCMNotification(api_key=settings.FCM_API_KEY)
                
                # Enviar notificación al dispositivo
                result = push_service.notify_single_device(
                    registration_id=user.fcmtoken.token,
                    message_title=message["title"],
                    message_body=message["body"],
                    data_message={
                        "type": "login",
                        "timestamp": message["timestamp"]
                    }
                )
                
                # Registrar el envío en la base de datos
                if result.get('success', 0) == 1:
                    print(f"Notificación FCM enviada a {user.username}")
                else:
                    print(f"Error al enviar FCM a {user.username}: {result}")
        
        except Exception as e:
            print(f"Error en FCM para {user.username}: {str(e)}")
    
    def send_web_push_notification(self, user, message):
        """Envía notificación Web Push a navegadores"""
        try:
            # Obtener todos los dispositivos registrados del usuario
            devices = Devices.objects.filter(user=user)
            
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
                        data=json.dumps({
                            "notification": message,
                            "data": {
                                "type": "login",
                                "timestamp": message["timestamp"],
                                "url": "/profile/"  # URL para redireccionar al hacer clic
                            }
                        }),
                        vapid_private_key=settings.VAPID_PRIVATE_KEY,
                        vapid_claims={
                            "sub": f"mailto:{settings.CONTACT_EMAIL}",
                            "aud": "https://updates.push.services.mozilla.com"
                        }
                    )
                    print(f"Notificación WebPush enviada a {user.username}")
                
                except WebPushException as e:
                    print(f"Error WebPush para {user.username}: {str(e)}")
                    # Opcional: eliminar dispositivo si el token es inválido
                    if "410" in str(e):  # Gone status
                        device.delete()
        
        except Exception as e:
            print(f"Error general en WebPush para {user.username}: {str(e)}")

def dashboard(request):
    #if not request.user.profile.
    return render(request, "users/dashboard.html")

  

def home_page(request):
    total_dispositivos = DispositivoInventario.objects.count()
    total_usuarios = User.objects.count()
    dispositivos_activos = DispositivoInventario.objects.filter(estado="Activo").count()
    context = {
        'active_tab': 'home',
        'total_dispositivos' : total_dispositivos,
        'total_usuarios' : total_usuarios, 
        'dispositivos_activos' : dispositivos_activos
    }
    return render(request, "home_page.html",  context)



def inventario_view(request):
    dispositivos = DispositivoInventario.objects.all()  # Obtener todos los dispositivos
    
    return render(request, 'inventario.html', {
        'dispositivos': dispositivos, 
        'active_tab': 'inventario'
    })

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import permission_required
User = get_user_model()

def is_superadmin_or_admin(user):
    return user.role in ['superadmin', 'admin'] or user.is_superuser

@login_required
@user_passes_test(is_superadmin_or_admin)
def usuarios(request):
    users = User.objects.all()
    return render(request, 'usuarios.html', {'users': users})


from rest_framework.permissions import IsAuthenticated
from .models import DispositivoInventario
from .serializers import DispositivoInventarioSerializer

class DispositivoInventarioCreateView(generics.CreateAPIView):
    queryset = DispositivoInventario.objects.all()
    serializer_class = DispositivoInventarioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError


@login_required
def agregar_dispositivo(request):
    usuarios_disponibles = User.objects.all() 
    if request.method == 'POST':
        try:
            
            
            # Validación manual
            if not request.POST.get('serial_number'):
                raise ValidationError('El número de serie es requerido')
            
            responsable_id = request.POST.get('responsable')
            responsable = User.objects.get(id=responsable_id) if responsable_id else None


            dispositivo = DispositivoInventario(
                numero_inventario=request.POST['inventory_number'],
                tipo=request.POST['tipo'],
                marca=request.POST['brand'],
                modelo=request.POST['model'],
                serial=request.POST['serial_number'],
                ubicacion=request.POST['location'],
                fecha_adquisicion=request.POST['acquisition_date'],
                estado=request.POST['status'],
                responsable=responsable,
                creado_por=request.user
            )
            
            dispositivo.full_clean()  # Valida todos los campos
            dispositivo.save()
            
            messages.success(request, '✅ Dispositivo agregado correctamente!')
            return redirect('inventario')
            
        except Exception as e:
            messages.error(request, f'❌ Error: {str(e)}')
            print("Error al guardar:", str(e))  # Log para depuración
    
    return render(request, 'inventario.html', {'usuarios': usuarios_disponibles})
from django.core.paginator import Paginator
import logging
from openpyxl import Workbook
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone
logger = logging.getLogger(__name__)
@login_required
def lista_dispositivos(request):
    # 1. Verificar consulta a la base de datos
    dispositivos = DispositivoInventario.objects.all()
    
    
    # 2. Verificar contexto enviado al template
    context = {'dispositivos': dispositivos}
    print(f"DEBUG - Contexto enviado: {context}")
    
    return render(request, 'devices_list.html', context)
from .models import DispositivoInventario, Backup, User

from django.contrib.auth import logout
def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
def reports_backups_view(request):
    # Obtener todos los usuarios para el filtro de reportes
    usuarios = User.objects.all()
    
    # Obtener backups existentes
    backups = Backup.objects.all().order_by('-fecha_creacion')
    
    # Inicializar resultados de reportes
    dispositivos_filtrados = None
    report_filters = {}
    
    # Manejar generación de reportes
    if request.method == 'POST' and 'report_type' in request.POST:
        # Obtener parámetros del formulario
        report_type = request.POST.get('report_type')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        estado = request.POST.get('estado')
        ubicacion = request.POST.get('ubicacion')
        usuario_id = request.POST.get('usuario')

        report_filters = {
            'report_type': report_type,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'estado': estado,
            'ubicacion': ubicacion,
            'usuario_id': usuario_id,
        }
        request.session['report_filters'] = report_filters


        # Filtrar dispositivos
        dispositivos = DispositivoInventario.objects.all()
        
        # Aplicar filtros según los parámetros
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                dispositivos = dispositivos.filter(
                    fecha_adquisicion__range=[fecha_inicio_dt, fecha_fin_dt]
                )
            except ValueError:
                messages.error(request, 'Formato de fecha inválido')
        
        if estado:
            dispositivos = dispositivos.filter(estado=estado)
        
        if ubicacion:
            dispositivos = dispositivos.filter(ubicacion=ubicacion)
        
        if usuario_id:
            usuario = User.objects.get(id=usuario_id)
            dispositivos = dispositivos.filter(responsable=usuario.username)
        
        dispositivos_filtrados = dispositivos
    
    elif 'report_filters' in request.session:
        report_filters = request.session['report_filters']
        dispositivos = DispositivoInventario.objects.all()
        
        if report_filters.get('fecha_inicio') and report_filters.get('fecha_fin'):
            try:
                fecha_inicio_dt = parse_date(report_filters['fecha_inicio'])
                fecha_fin_dt = parse_date(report_filters['fecha_fin'])
                if fecha_inicio_dt and fecha_fin_dt:
                    dispositivos = dispositivos.filter(
                        fecha_adquisicion__range=[fecha_inicio_dt, fecha_fin_dt]
                    )
            except (ValueError, TypeError):
                pass
        
        if report_filters.get('estado'):
            dispositivos = dispositivos.filter(estado=report_filters['estado'])
        
        if report_filters.get('ubicacion'):
            dispositivos = dispositivos.filter(ubicacion=report_filters['ubicacion'])
        
        if report_filters.get('usuario_id'):
            try:
                usuario = User.objects.get(id=report_filters['usuario_id'])
                dispositivos = dispositivos.filter(responsable=usuario.username)
            except User.DoesNotExist:
                pass

        dispositivos_filtrados = dispositivos

    export_format = request.GET.get('export')
    if export_format and dispositivos_filtrados:
        if export_format == 'pdf':
            return generate_pdf_report(dispositivos_filtrados)
        elif export_format == 'excel':
            return generate_excel_report(dispositivos_filtrados)

    
    # Manejar creación de backups
    if request.method == 'POST' and 'backup_type' in request.POST:
        backup_type = request.POST.get('backup_type')
        description = request.POST.get('description', '')
        
        try:
            backup = Backup.objects.create(
            tipo=backup_type,
            descripcion=description,
            tamaño=1024 * 1024,  # 1MB de ejemplo
            ubicacion="/backups/real/",
            creado_por=request.user
            )
            messages.success(request, f'Backup {backup_type} creado exitosamente')
            backup.save()
            # Actualizar la lista de backups
            backups = Backup.objects.all().none()
        except Exception as e:
            messages.error(request, f'Error al crear backup: {str(e)}')
    
    context = {
        'usuarios': usuarios,
        'dispositivos': dispositivos_filtrados,
        'backups': backups,
        'active_tab': 'reports_backups',
        'current_filters': report_filters
    }
    return render(request, 'reports_backups.html', context)

from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from io import BytesIO

def generate_pdf_report(dispositivos):
    try:
        # Configurar el buffer y el documento
        buffer = BytesIO()
        
        # Usar SimpleDocTemplate para mejor control
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),  # Horizontal para tablas anchas
            rightMargin=inch/2,
            leftMargin=inch/2,
            topMargin=inch/2,
            bottomMargin=inch/2
        )
        
        # Estilos
        styles = getSampleStyleSheet()
        title_style = styles['Title']
        title_style.alignment = 1  # Centrado
        
        # Contenido del PDF
        elements = []
        
        # 1. Título
        elements.append(Paragraph("REPORTE DE INVENTARIO", title_style))
        elements.append(Spacer(1, 12))
        
        # 2. Tabla de datos
        data = [
            ["N° Inventario", "Tipo", "Marca", "Modelo", "Serial", "Ubicación", "Estado", "Responsable"]
        ]
        
        # Llenar datos
        for dispositivo in dispositivos:
            data.append([
                dispositivo.numero_inventario,
                dispositivo.get_tipo_display(),
                dispositivo.marca,
                dispositivo.modelo,
                dispositivo.serial,
                dispositivo.ubicacion,
                dispositivo.estado,
                dispositivo.responsable
            ])
        
        # Crear tabla con estilo
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2E7D32')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 12))
        
        # 3. Pie de página
        elements.append(Paragraph(
            f"Total de dispositivos: {len(dispositivos)} | Generado el: {timezone.now().strftime('%d/%m/%Y %H:%M')}",
            styles['Normal']
        ))
        
        # Construir PDF
        doc.build(elements)
        
        # Configurar respuesta HTTP
        pdf = buffer.getvalue()
        buffer.close()
        
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'
        response.write(pdf)
        
        return response
        
    except Exception as e:
        logger.error(f"Error generando PDF: {str(e)}")
        return HttpResponse(f"Error al generar PDF: {str(e)}", status=500)
    

def generate_excel_report(dispositivos):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"reporte_inventario_{timezone.now().strftime('%Y%m%d_%H%M')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Inventario"
    
    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color='2E7D32', end_color='2E7D32', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    # Encabezados
    headers = ['N° Inventario', 'Tipo', 'Marca', 'Modelo', 'Serial', 'Ubicación', 'Estado', 'Responsable']
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        cell = ws[f'{col_letter}1']
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    
    # Datos
    for row_num, dispositivo in enumerate(dispositivos, 2):
        ws.cell(row=row_num, column=1, value=dispositivo.numero_inventario)
        ws.cell(row=row_num, column=2, value=dispositivo.get_tipo_display())
        ws.cell(row=row_num, column=3, value=dispositivo.marca)
        ws.cell(row=row_num, column=4, value=dispositivo.modelo)
        ws.cell(row=row_num, column=5, value=dispositivo.serial)
        ws.cell(row=row_num, column=6, value=dispositivo.ubicacion)
        ws.cell(row=row_num, column=7, value=dispositivo.estado)
        ws.cell(row=row_num, column=8, value=dispositivo.responsable)
        
        # Alternar colores de fila
        if row_num % 2 == 0:
            fill_color = 'F5F9F5'
        else:
            fill_color = 'FFFFFF'
        
        for col in range(1, 9):
            ws.cell(row=row_num, column=col).fill = PatternFill(
                start_color=fill_color, 
                end_color=fill_color, 
                fill_type='solid'
            )
    
    # Ajustar anchos de columna
    column_widths = [20, 15, 15, 25, 20, 25, 15, 20]
    for i, width in enumerate(column_widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = width
    
    # Congelar encabezados
    ws.freeze_panes = 'A2'
    
    # Añadir información de generación
    ws.append([])
    ws.append(['Información del reporte:'])
    ws.append([f'Fecha de generación: {timezone.now().strftime("%d/%m/%Y %H:%M")}'])
    ws.append([f'Total de dispositivos: {len(dispositivos)}'])
    
    wb.save(response)
    return response

# Modificar export_report para usar filtros persistentes
@login_required
def export_report(request, format):
    # Obtener filtros de la sesión
    report_filters = request.session.get('report_filters', {})
    
    dispositivos = DispositivoInventario.objects.all()
    
    # Aplicar filtros
    if report_filters.get('fecha_inicio') and report_filters.get('fecha_fin'):
        try:
            fecha_inicio_dt = parse_date(report_filters['fecha_inicio'])
            fecha_fin_dt = parse_date(report_filters['fecha_fin'])
            if fecha_inicio_dt and fecha_fin_dt:
                dispositivos = dispositivos.filter(
                    fecha_adquisicion__range=[fecha_inicio_dt, fecha_fin_dt]
                )
        except (ValueError, TypeError):
            pass
    
    if report_filters.get('estado'):
        dispositivos = dispositivos.filter(estado=report_filters['estado'])
    
    if report_filters.get('ubicacion'):
        dispositivos = dispositivos.filter(ubicacion=report_filters['ubicacion'])
    
    if report_filters.get('usuario_id'):
        try:
            usuario = User.objects.get(id=report_filters['usuario_id'])
            dispositivos = dispositivos.filter(responsable=usuario.username)
        except User.DoesNotExist:
            pass
    
    # Generar reporte según formato
    if format == 'pdf':
        return generate_pdf_report(dispositivos)
    elif format == 'excel':
        return generate_excel_report(dispositivos)
    
    return redirect('reports_backups')

# Vista para descargar backup (simulada)
@login_required
def download_backup(request, backup_id):
    try:
        backup = Backup.objects.get(id=backup_id)
        # En producción, serviríamos el archivo real
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="backup_{backup_id}.bak"'
        # Aquí iría el contenido real del backup
        response.write(b"Simulated backup content")
        return response
    except Backup.DoesNotExist:
        messages.error(request, 'Backup no encontrado')
        return redirect('reports_backups')


# Vista para restaurar backup (simulada)
@login_required
def restore_backup(request, backup_id):
    try:
        backup = Backup.objects.get(id=backup_id)
        # En producción, aquí se restauraría el backup real
        messages.success(request, f'Backup #{backup_id} restaurado exitosamente')
    except Backup.DoesNotExist:
        messages.error(request, 'Backup no encontrado')
    
    return redirect('reports_backups')
from .models import Mantenimiento
@login_required
def mantenimiento_view(request):
    mantenimientos = Mantenimiento.objects.all().prefetch_related('dispositivo')
    dispositivos = DispositivoInventario.objects.all()
    usuarios = User.objects.filter(is_active=True)
    
    return render(request, 'mantenimiento.html', {
        'mantenimientos': mantenimientos,
        'dispositivos': dispositivos,
        'usuarios': usuarios,
        'active_tab': 'mantenimiento'
    })








def test_firestore_connection(db):
        try:
            doc_ref = db.collection("test_collection").document("test_doc")
            doc_ref.set({"message": "Hello from Django emulator!"})
            return True, "Successfully connected to Firestore emulator!"
        except Exception as e:
            return False, f"Error connecting to Firestore emulator: {e}"
        

def my_view(request):
    try:
        app, db, auth_client = initialize_firebase()

        if not test_firestore_connection(db):
            raise Exception("Failed to connect to Firestore emulator!") #Raise exception.

        # Load configuration from JSON file
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Project root
        config_file_path = os.path.join(base_dir, '..', 'etc', 'config.json')

        with open(config_file_path, 'r') as f:
            config = json.load(f)

        user_email = config['FIREBASE_SECRETS']['user_email']
        user_password = config['FIREBASE_SECRETS']['user_password']

        # Example: Create a user in the Authentication emulator
        try:
            user = auth_client.create_user(
                email=user_email,
                password=user_password
            )
            print(f'Successfully created new user: {user.uid}')
        except Exception as e:
            print(f"Error creating user: {e}")

        # Example: Write data to Firestore emulator
        doc_ref = db.collection("users").document("alovelace")
        doc_ref.set({"first": "Ada", "last": "Lovelace", "born": 1815})

        return HttpResponse("Firebase interactions complete!")
    except FileNotFoundError as e:
        return HttpResponse(f"Config file error: {e}", status=500)
    except Exception as e:
        return HttpResponse(f"Error initializing Firebase: {e}", status=500)
    


def push_notifications_view(request):
    return render(request, 'push/push_notifications.html')

@csrf_exempt  # Disable CSRF protection for this view (for testing purposes only!)
def send_login_notification(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Usuario no autenticado'
                }, status=401)
            
            # Verificar si el usuario tiene token FCM
            try:
                fcm_token = FCMToken.objects.get(user=request.user, is_active=True)
            except FCMToken.DoesNotExist:
                return JsonResponse({
                    'status': 'error',
                    'message': 'No hay token FCM registrado para este usuario'
                }, status=400)
            
            # Configurar FCM
            push_service = FCMNotification(api_key=settings.FCM_API_KEY)
            
            # Enviar notificación
            result = push_service.notify_single_device(
                registration_id=fcm_token.token,
                message_title="Nuevo inicio de sesión",
                message_body=f"Usuario {request.user.username} ha iniciado sesión",
                data_message={
                    "type": "login",
                    "timestamp": str(timezone.now()),
                    "url": "/dashboard/"
                }
            )
            
            return JsonResponse({
                'status': 'success',
                'result': result,
                'message': 'Notificación enviada'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'status': 'error',
        'message': 'Método no permitido'
    }, status=405)
def csrf_failure_view(request, reason=""):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'message': 'CSRF verification failed',
            'reason': reason
        }, status=403)
    # Fallback para solicitudes no-AJAX
    from django.views.csrf import csrf_failure
    return csrf_failure(request, reason=reason)

def save_token(request):
    if request.method == 'POST' and request.user.is_authenticated:
        try:
            data = json.loads(request.body.decode('utf-8'))
            token = data.get('token')

            if not token:
                return JsonResponse({'success': False, 'message': 'Token is required'}, status=400)

            # Actualizar o crear el token para el usuario actual
            FCMToken.objects.update_or_create(
                user=request.user,
                defaults={
                    'token': token,
                    'is_active': True,
                    'device_name': data.get('device_name', 'Unknown')
                }
            )

            return JsonResponse({'success': True, 'message': 'Token saved successfully!'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    return JsonResponse({'success': False, 'message': 'Authentication required'}, status=401)



@login_required
def check_fcm_token(request):
    try:
        has_token = FCMToken.objects.filter(user=request.user, is_active=True).exists()
        return JsonResponse({
            'status': 'success',
            'hasToken': has_token,
            'message': 'Token verificado'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
@login_required
def check_auth(request):
    return JsonResponse({'isAuthenticated': True})

@login_required
def check_fcm_token(request):
    has_token = FCMToken.objects.filter(user=request.user, is_active=True).exists()
    return JsonResponse({'hasToken': has_token})
@login_required      
def send_profile_visit_notification(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username", request.user.username)

            from users.models import Device
            devices = Device.objects.filter(user=request.user)

            visit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            message = {
                "title": f"Profile Visit Notification",
                "body": f"{username} visited profile a {visit_time}",
                "icon": "/static/images/icon.png"
            }

            for device in devices:
                try:
                    webpush(subscription_info={
                        "endpoint": device.endpoint,
                        "keys": {
                            "p265dh": device.p265dh,
                            "auth": device.auth
                        }
                    },
                    data= json.dumps(message),
                    vapid_private_key=settings.VAPID_PRIVATE_KEY,
                    vapid_claims={
                        "sub": f"mailto:{settings.FIREBASE_SECRETS.get('user_email', 'alextoledo2602@gmail.com')}"
                    })
                except WebPushException as ex:
                    print("Error al enviar notificacion", ex)
            return JsonResponse({"status": "Success"})
        except Exception as e:
            return JsonResponse({"status": "Error", "message": str(e)}, status=400)
    return JsonResponse({"status": "Error", "message": "Invalid request method"}, status=405)
@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})
@login_required
def send_login_notification(request):
    if request.method == 'POST':
        try:
            user = request.user
            login_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            message = {
                "title": "Nuevo inicio de sesión",
                "body": f"El usuario {user.username} inició sesión el {login_time}",
                "icon": "/static/images/icon.png",
                "timestamp": login_time
            }
            print(f"Token FCM del usuario: {user.fcmtoken.token}")  # Debug
            
            push_service = FCMNotification(api_key=settings.FCM_API_KEY)
            response = push_service.notify_single_device(
                registration_id=user.fcmtoken.token,
                message_title="Prueba de notificación",
                message_body="Esta es una notificación de prueba",
                data_message={"url": "/dashboard/"}
            )
            
            print("Respuesta de FCM:", response)
            # Enviar notificación FCM
            if hasattr(user, 'fcmtoken') and user.fcmtoken.is_active:
                push_service = FCMNotification(api_key=settings.FCM_API_KEY)
                result = push_service.notify_single_device(
                    registration_id=user.fcmtoken.token,
                    message_title=message["title"],
                    message_body=message["body"],
                    data_message={
                        "type": "login",
                        "timestamp": message["timestamp"],
                        "url": "/accounts/dashboard/"
                    }
                )
                print("Resultado FCM:", result)
            
            # Enviar notificación Web Push
            devices = Devices.objects.filter(user=user)
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
                        data=json.dumps({
                            "notification": message,
                            "data": {
                                "type": "login",
                                "timestamp": message["timestamp"],
                                "url": "/accounts/dashboard/"
                            }
                        }),
                        vapid_private_key=settings.VAPID_PRIVATE_KEY,
                        vapid_claims={
                            "sub": f"mailto:{settings.CONTACT_EMAIL}",
                            "aud": "https://updates.push.services.mozilla.com"
                        }
                    )
                except WebPushException as e:
                    print("Error WebPush:", e)
                    if "410" in str(e):
                        device.delete()
            
            return JsonResponse({"status": "success", "message": "Notificaciones enviadas"})
        
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
