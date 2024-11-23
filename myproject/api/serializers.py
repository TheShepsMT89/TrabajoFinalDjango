from django.contrib.auth import authenticate
from rest_framework import serializers
from api.models import *

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    contraseña = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            usuario = Usuario.objects.get(email=data['email'])
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Usuario no encontrado')

        # Usar check_password para verificar la contraseña
        if not usuario.check_password(data['contraseña']):
            raise serializers.ValidationError('Credenciales inválidas')

        return {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'email': usuario.email,
            'rol': usuario.rol,
        }
    
from .models import Factura_cliente, Factura_proveedor

class FacturaClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura_cliente
        fields = ['id', 'numero_factura', 'estado', 'fecha_vencimiento']  # Incluye 'estado' y 'fecha_vencimiento'.

class FacturaProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura_proveedor
        fields = ['id', 'numero_factura', 'estado', 'fecha_vencimiento']