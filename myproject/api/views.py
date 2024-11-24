from datetime import timedelta
from django.shortcuts import render
from django.core.mail import send_mail
from .models import Cliente, Proveedor
from .serializers import ClienteSerializer, ProveedorSerializer
from .serializers import UsuarioSerializer
# Create your views here.
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import FacturaClienteSerializer, FacturaProveedorSerializer, LoginSerializer
from api.serializers import LoginSerializer
from api.models import Usuario
from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import EsAdmin
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Factura_cliente, Factura_proveedor
from .permissions import EsContador

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import ModelViewSet

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            usuario_data = serializer.validated_data
            usuario = Usuario.objects.get(email=usuario_data['email'])

            # Generar tokens JWT
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'rol': usuario_data['rol'],
                'nombre': usuario_data['nombre'],
            })
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    def post(self, request):
        # Solo es necesario que el frontend elimine el token localmente
        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie('access_token')  # Eliminar cookie si se usa
        return response



class VistaSoloAdmin(APIView):
    permission_classes = [EsAdmin]

    def get(self, request):
        return Response({"mensaje": "Acceso solo para administradores."})


def enviar_correo(destinatario, asunto, mensaje):
    send_mail(
        asunto,
        mensaje,
        'no-reply@tudominio.com',  # Correo del remitente
        [destinatario],  # Lista de destinatarios
        fail_silently=False,
    )

class FacturaClienteViewSet(ModelViewSet):
    queryset = Factura_cliente.objects.all()
    serializer_class = FacturaClienteSerializer
    permission_classes = [IsAuthenticated, EsContador]

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        factura = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado in dict(Factura_cliente.ESTADO_CHOICES):
            factura.estado = nuevo_estado
            factura.save()
            return Response({"mensaje": f"Estado cambiado a {nuevo_estado}"}, status=status.HTTP_200_OK)
        return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

    # Método para recuperar notificaciones de facturas vencidas o próximas a vencer
    @action(detail=False, methods=['get'])
    def notificaciones(self, request):
        facturas_proximas = self.queryset.filter(
            fecha_vencimiento__lte=now() + timedelta(days=3), estado='pendiente'
        )
        facturas_vencidas = self.queryset.filter(
            fecha_vencimiento__lte=now(), estado='pendiente'
        )

        # Enviar correo para facturas próximas a vencer
        for factura in facturas_proximas:
            enviar_correo(
                factura.cliente.email, 
                f"Factura {factura.numero_factura} próxima a vencer",
                f"La factura {factura.numero_factura} está próxima a vencer el {factura.fecha_vencimiento}. Por favor, realiza el pago antes de la fecha límite."
            )
        
        # Enviar correo para facturas vencidas
        for factura in facturas_vencidas:
            enviar_correo(
                factura.cliente.email, 
                f"Factura {factura.numero_factura} vencida",
                f"La factura {factura.numero_factura} está vencida desde el {factura.fecha_vencimiento}. Por favor, realiza el pago lo antes posible."
            )

        # Responder con los datos de las facturas
        data = {
            "proximas_a_vencer": [
                {"id": f.id, "numero_factura": f.numero_factura, "fecha_vencimiento": f.fecha_vencimiento}
                for f in facturas_proximas
            ],
            "vencidas": [
                {"id": f.id, "numero_factura": f.numero_factura, "fecha_vencimiento": f.fecha_vencimiento}
                for f in facturas_vencidas
            ]
        }
        return Response(data, status=status.HTTP_200_OK)

class FacturaProveedorViewSet(ModelViewSet):
    queryset = Factura_proveedor.objects.all()
    serializer_class = FacturaProveedorSerializer
    permission_classes = [IsAuthenticated, EsContador]

    @action(detail=True, methods=['patch'])
    def cambiar_estado(self, request, pk=None):
        factura = self.get_object()
        nuevo_estado = request.data.get('estado')
        if nuevo_estado in dict(Factura_proveedor.ESTADO_CHOICES):
            factura.estado = nuevo_estado
            factura.save()
            return Response({"mensaje": f"Estado cambiado a {nuevo_estado}"}, status=status.HTTP_200_OK)
        return Response({"error": "Estado inválido"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def notificaciones(self, request):
        facturas_proximas = self.queryset.filter(
            fecha_vencimiento__lte=now() + timedelta(days=3), estado='pendiente'
        )
        facturas_vencidas = self.queryset.filter(
            fecha_vencimiento__lte=now(), estado='pendiente'
        )

        # Enviar correo para facturas próximas a vencer
        for factura in facturas_proximas:
            enviar_correo(
                factura.proveedor.email, 
                f"Factura {factura.numero_factura} próxima a vencer",
                f"La factura {factura.numero_factura} está próxima a vencer el {factura.fecha_vencimiento}. Por favor, realiza el pago antes de la fecha límite."
            )
        
        # Enviar correo para facturas vencidas
        for factura in facturas_vencidas:
            enviar_correo(
                factura.proveedor.email, 
                f"Factura {factura.numero_factura} vencida",
                f"La factura {factura.numero_factura} está vencida desde el {factura.fecha_vencimiento}. Por favor, realiza el pago lo antes posible."
            )

        # Responder con los datos de las facturas
        data = {
            "proximas_a_vencer": [
                {"id": f.id, "numero_factura": f.numero_factura, "fecha_vencimiento": f.fecha_vencimiento}
                for f in facturas_proximas
            ],
            "vencidas": [
                {"id": f.id, "numero_factura": f.numero_factura, "fecha_vencimiento": f.fecha_vencimiento}
                for f in facturas_vencidas
            ]
        }
        return Response(data, status=status.HTTP_200_OK)



class ClienteViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]  # Ajusta las clases de permisos según tus necesidades

class ProveedorViewSet(ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Usuario
from .serializers import UsuarioSerializer

class UsuarioLogueadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario = request.user
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)