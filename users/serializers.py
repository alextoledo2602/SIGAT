# users/serializers.py
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLES)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'role', 'password', 'groups']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Extract role and groups from validated_data
        role = validated_data.pop('role', "invitado")
        #password = validated_data.pop('password', None)
        groups_data = validated_data.pop('groups', [])

        # Create user instance without password and groups
        user = User.objects.create_user(role=role,**validated_data)
        # Extract role and groups from validated_data
        
    
    # Asignación directa de grupos
        if role == 'superadmin':
            group = Group.objects.get(name='Superadministradores')
            user.groups.add(group)
            user.is_superuser = True
            user.is_staff = True
        elif role == 'admin':
            group = Group.objects.get(name='Administradores')
            user.groups.add(group)
            user.is_staff = True
    
        user.save()
        return user

from .models import DispositivoInventario

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