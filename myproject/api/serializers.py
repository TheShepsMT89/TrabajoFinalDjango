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
    # Campos adicionales para los nombres
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Factura_cliente
        fields = [
            'id', 'numero_factura', 'estado', 'fecha_vencimiento', 'monto', 'descripcion', 
            'fecha', 'cliente', 'usuario', 'cliente_nombre', 'usuario_nombre'
        ]


class FacturaProveedorSerializer(serializers.ModelSerializer):
    # Campos adicionales para los nombres
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Factura_proveedor
        fields = ['id', 'numero_factura', 'estado', 'fecha_vencimiento', 'monto', 'descripcion', 'fecha', 'proveedor', 'usuario', 'proveedor_nombre', 'usuario_nombre']



from rest_framework import serializers
from .models import Cliente, Proveedor

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


        from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'