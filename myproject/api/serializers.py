from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Usuario, Cliente, Proveedor, Factura_Cliente, Factura_Proveedor, AuditLog

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

class FacturaClienteSerializer(serializers.ModelSerializer):
    # Campos adicionales para los nombres
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Factura_Cliente  # Asegúrate de que esto sea Factura_Cliente (con mayúsculas)
        fields = [
            'id', 'numero_factura', 'estado', 'fecha_vencimiento', 'monto', 'descripcion', 
            'fecha', 'cliente', 'usuario', 'cliente_nombre', 'usuario_nombre', 'accion'
        ]

class FacturaProveedorSerializer(serializers.ModelSerializer):
    # Campos adicionales para los nombres
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True)

    class Meta:
        model = Factura_Proveedor  # Asegúrate de que esto sea Factura_Proveedor (con mayúsculas)
        fields = [
            'id', 'numero_factura', 'estado', 'fecha_vencimiento', 'monto', 'descripcion', 
            'fecha', 'proveedor', 'usuario', 'proveedor_nombre', 'usuario_nombre', 'accion'
        ]

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'

from .models import ReporteFactura  # Asegúrate de importar el modelo ReporteFactura

class ReporteFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteFactura
        fields = '__all__'


from .models import ReporteFactura  # Asegúrate de importar el modelo ReporteFactura

class ReporteFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteFactura
        fields = '__all__'