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
        fields = ['id', 'nombre', 'email', 'telefono', 'direccion', 'creado_por']

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'email', 'telefono', 'direccion', 'creado_por']
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class UsuarioDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'password', 'rol', 'telefono', 'direccion']  # Campos requeridos
        extra_kwargs = {
            'password': {'write_only': True}  # La contraseña solo puede escribirse
        }  

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






from rest_framework import serializers
from .models import SimpleMessage

class SimpleMessageSerializer(serializers.ModelSerializer):
    user_nombre = serializers.CharField(source='user.nombre', read_only=True)
    user_avatar = serializers.URLField(source='user.avatar', read_only=True)

    class Meta:
        model = SimpleMessage
        fields = ['id', 'user', 'user_nombre', 'user_avatar', 'content']



from rest_framework import serializers
from .models import Usuario, Factura_Cliente, Factura_Proveedor

class UsuarioFacturaSerializer(serializers.ModelSerializer):
    total_facturas_cliente = serializers.IntegerField()
    total_facturas_proveedor = serializers.IntegerField()

    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email', 'rol', 'total_facturas_cliente', 'total_facturas_proveedor']



class UsuarioListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'email']  # Campos visibles en el listado




from rest_framework import serializers
from .models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    rol= serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['nombre', 'password', 'email', 'rol']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        rol = validated_data.pop('rol')
        user = Usuario.objects.create_user(
            email=validated_data['email'],
            nombre=validated_data['nombre'],
            password=validated_data['password'],
            rol=rol
        )
        return user