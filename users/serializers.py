# users/serializers.py
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLES)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'id': {'required': True, 'read_only': False},
            'email': {'required': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        # Extraer campos necesarios
        password = validated_data.pop('password')
        role = validated_data.pop('role', 'invitado')
        
        # Crear usuario usando el CustomUserManager
        user = User.objects.create_user(
            id=validated_data['id'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=password,
            role=role,
            **{k: v for k, v in validated_data.items() if k in ['first_name', 'last_name']}
        )
        return user

from .models import DispositivoInventario, Mantenimiento, Backup

class DispositivoInventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispositivoInventario
        fields = '__all__'
        read_only_fields = ('creado_por', 'fecha_creacion')

    def validate_serial(self, value):
        """Valida que el serial sea único"""
        if DispositivoInventario.objects.filter(serial=value).exists():
            raise serializers.ValidationError("Este número de serie ya está registrado")
        return value
class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = '__all__'

class MantenimientoSerializer(serializers.ModelSerializer):
    dispositivo = DispositivoInventarioSerializer(read_only=True)
    
    class Meta:
        model = Mantenimiento
        fields = '__all__'