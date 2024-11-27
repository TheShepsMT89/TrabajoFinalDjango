from datetime import timedelta
from django.shortcuts import render
from django.core.mail import send_mail
from .models import Cliente, Proveedor
from .serializers import ClienteSerializer, ProveedorSerializer
from .serializers import UsuarioSerializer
# Create your views here.

from .models import Factura_Cliente,Factura_Proveedor


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
    queryset = Factura_Cliente.objects.all()
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
    queryset = Factura_Proveedor.objects.all()
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


class ClienteAdminViewSet(ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]

class ProveedorAdminViewSet(ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]

class FacturaClienteAdminViewSet(ModelViewSet):
    queryset = Factura_Cliente.objects.all()
    serializer_class = FacturaClienteSerializer
    permission_classes = [IsAuthenticated]

class FacturaProveedorAdminViewSet(ModelViewSet):
    queryset = Factura_Proveedor.objects.all()
    serializer_class = FacturaProveedorSerializer
    permission_classes = [IsAuthenticated]


from .serializers import UsuarioListSerializer, UsuarioDetailSerializer
class UsuarioAdminViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    permission_classes = [IsAuthenticated, EsAdmin]

    # Selección dinámica del serializador
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsuarioListSerializer
        return UsuarioDetailSerializer

    # Método para cambiar el rol desde React
    @action(detail=True, methods=['patch'])
    def cambiar_rol(self, request, pk=None):
        usuario = self.get_object()
        nuevo_rol = request.data.get('rol')
        if nuevo_rol in ['admin', 'contador', 'gerente']:  # Valida los roles disponibles
            usuario.rol = nuevo_rol
            usuario.save()
            return Response({"mensaje": f"Rol cambiado a {nuevo_rol}"})
        return Response({"error": "Rol inválido"}, status=400)


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

    def get(self, request, *args, **kwargs):
        usuario = request.user
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        usuario = request.user
        serializer = UsuarioSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)



from rest_framework import viewsets
from .models import Cliente, Proveedor, AuditLog
from .serializers import FacturaClienteSerializer, FacturaProveedorSerializer, ClienteSerializer, ProveedorSerializer, AuditLogSerializer
from rest_framework.permissions import IsAuthenticated

class FacturaClienteViewSet(viewsets.ModelViewSet):
    queryset = Factura_Cliente.objects.all()
    serializer_class = FacturaClienteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        factura = serializer.save()
        AuditLog.objects.create(user=self.request.user, action="FacturaCliente creada", details=f"FacturaCliente ID: {factura.id}")

    def perform_update(self, serializer):
        factura = serializer.save()
        AuditLog.objects.create(user=self.request.user, action="FacturaCliente actualizada", details=f"FacturaCliente ID: {factura.id}")

    def perform_destroy(self, instance):
        AuditLog.objects.create(user=self.request.user, action="FacturaCliente eliminada", details=f"FacturaCliente ID: {instance.id}")
        instance.delete()

class FacturaProveedorViewSet(viewsets.ModelViewSet):
    queryset = Factura_Proveedor.objects.all()
    serializer_class = FacturaProveedorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        factura = serializer.save()
        AuditLog.objects.create(user=self.request.user, action="FacturaProveedor creada", details=f"FacturaProveedor ID: {factura.id}")

    def perform_update(self, serializer):
        factura = serializer.save()
        AuditLog.objects.create(user=self.request.user, action="FacturaProveedor actualizada", details=f"FacturaProveedor ID: {factura.id}")

    def perform_destroy(self, instance):
        AuditLog.objects.create(user=self.request.user, action="FacturaProveedor eliminada", details=f"FacturaProveedor ID: {instance.id}")
        instance.delete()

# Define otros ViewSets y vistas aquí

from rest_framework import generics
from .models import AuditLog
from .serializers import AuditLogSerializer
from rest_framework.permissions import IsAuthenticated

class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]


from .models import ReporteFactura  # Asegúrate de importar el modelo ReporteFactura
from .serializers import ReporteFacturaSerializer  # Asegúrate de importar el serializador ReporteFacturaSerializer

class ReporteFacturaViewSet(viewsets.ModelViewSet):
    queryset = ReporteFactura.objects.all()
    serializer_class = ReporteFacturaSerializer
    permission_classes = [IsAuthenticated]



from rest_framework import viewsets
from .models import SimpleMessage
from .serializers import SimpleMessageSerializer
from rest_framework.permissions import IsAuthenticated

class SimpleMessageViewSet(viewsets.ModelViewSet):
    queryset = SimpleMessage.objects.all()
    serializer_class = SimpleMessageSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Factura_Cliente, Factura_Proveedor
from django.db.models import Sum
from datetime import datetime

class TotalPorCobrarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_por_cobrar = Factura_Cliente.objects.filter(estado='pendiente').aggregate(total=Sum('monto'))['total']
        return Response({'total_por_cobrar': total_por_cobrar})

class TotalPorPagarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_por_pagar = Factura_Proveedor.objects.filter(estado='pendiente').aggregate(total=Sum('monto'))['total']
        return Response({'total_por_pagar': total_por_pagar})

class FacturasVencidasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        hoy = datetime.now()
        facturas_vencidas_clientes = Factura_Cliente.objects.filter(fecha_vencimiento__lt=hoy, estado='pendiente')
        facturas_vencidas_proveedores = Factura_Proveedor.objects.filter(fecha_vencimiento__lt=hoy, estado='pendiente')
        return Response({
            'facturas_vencidas_clientes': facturas_vencidas_clientes.values(),
            'facturas_vencidas_proveedores': facturas_vencidas_proveedores.values()
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Factura_Cliente, Factura_Proveedor
from django.db.models import Sum
from datetime import datetime
from django.db.models.functions import TruncDay


class ProyeccionFlujoCajaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe proporcionar fecha_inicio y fecha_fin'}, status=400)
        
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        ingresos = Factura_Cliente.objects.filter(fecha__range=(fecha_inicio, fecha_fin)) \
            .annotate(dia=TruncDay('fecha')) \
            .values('dia') \
            .annotate(total=Sum('monto')) \
            .order_by('dia')

        egresos = Factura_Proveedor.objects.filter(fecha__range=(fecha_inicio, fecha_fin)) \
            .annotate(dia=TruncDay('fecha')) \
            .values('dia') \
            .annotate(total=Sum('monto')) \
            .order_by('dia')

        flujo_caja = []
        for ingreso, egreso in zip(ingresos, egresos):
            flujo_caja.append({
                'fecha': ingreso['dia'],
                'ingresos': ingreso['total'] or 0,
                'egresos': egreso['total'] or 0,
                'flujo_caja': (ingreso['total'] or 0) - (egreso['total'] or 0)
            })

        return Response(flujo_caja) 
    



class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)




from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Factura_Cliente, Factura_Proveedor, Cliente, Proveedor, Usuario
from .serializers import FacturaClienteSerializer, FacturaProveedorSerializer, ClienteSerializer, ProveedorSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def perform_create(self, serializer):
        serializer.save(creado_por=self.request.user)

class FacturaClienteViewSet(viewsets.ModelViewSet):
    queryset = Factura_Cliente.objects.all()
    serializer_class = FacturaClienteSerializer

class FacturaProveedorViewSet(viewsets.ModelViewSet):
    queryset = Factura_Proveedor.objects.all()
    serializer_class = FacturaProveedorSerializer

class TotalPorCobrarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_por_cobrar_clientes = Factura_Cliente.objects.filter(estado='pendiente').aggregate(total=Sum('monto'))['total'] or 0
        total_por_cobrar_proveedores = Factura_Proveedor.objects.filter(estado='pendiente').aggregate(total=Sum('monto'))['total'] or 0
        total_por_cobrar = total_por_cobrar_clientes + total_por_cobrar_proveedores
        return Response({'total_por_cobrar': total_por_cobrar})

class TotalPorPagarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_por_pagar_clientes = Factura_Cliente.objects.filter(estado='pendiente').aggregate(total=Sum('monto'))['total'] or 0
        total_por_pagar_proveedores = Factura_Proveedor.objects.filter(estado='pendiente').aggregate(total=Sum('monto'))['total'] or 0
        total_por_pagar = total_por_pagar_clientes + total_por_pagar_proveedores
        return Response({'total_por_pagar': total_por_pagar})
    
class FacturasVencidasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        hoy = timezone.now().date()
        facturas_vencidas_clientes = Factura_Cliente.objects.filter(fecha_vencimiento__lt=hoy, estado='pendiente').count()
        facturas_vencidas_proveedores = Factura_Proveedor.objects.filter(fecha_vencimiento__lt=hoy, estado='pendiente').count()
        total_facturas_vencidas = facturas_vencidas_clientes + facturas_vencidas_proveedores
        return Response({'facturas_vencidas': total_facturas_vencidas})

class ProyeccionFlujoCajaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe proporcionar fecha_inicio y fecha_fin'}, status=400)
        
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        ingresos = Factura_Cliente.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(total=Sum('monto'))['total']
        egresos = Factura_Proveedor.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(total=Sum('monto'))['total']

        flujo_caja = (ingresos or 0) - (egresos or 0)

        return Response({
            'ingresos': ingresos,
            'egresos': egresos,
            'flujo_caja': flujo_caja
        })

from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Usuario, Factura_Cliente, Factura_Proveedor
from .serializers import UsuarioFacturaSerializer

class TotalFacturasPorUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rol = request.query_params.get('rol', 'contador')
        usuarios = Usuario.objects.filter(rol=rol).annotate(
            total_facturas_cliente=Count('facturas_cliente', distinct=True),
            total_facturas_proveedor=Count('facturas_proveedor', distinct=True)
        )
        serializer = UsuarioFacturaSerializer(usuarios, many=True)
        return Response(serializer.data)
class NotificacionesFacturasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        hoy = timezone.now().date()
        proximas_vencer = Factura_Cliente.objects.filter(fecha_vencimiento__lte=hoy + timedelta(days=3), estado='pendiente').count()
        vencidas = Factura_Cliente.objects.filter(fecha_vencimiento__lt=hoy, estado='pendiente').count()
        return Response({
            'proximas_vencer': proximas_vencer,
            'vencidas': vencidas
        })
    


class TotalFacturasPorEstadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_facturas_cliente = Factura_Cliente.objects.values('estado').annotate(total=Count('estado'))
        total_facturas_proveedor = Factura_Proveedor.objects.values('estado').annotate(total=Count('estado'))
        return Response({
            'total_facturas_cliente': total_facturas_cliente,
            'total_facturas_proveedor': total_facturas_proveedor
        })
    


class TotalMontoPorEstadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_monto_cliente = Factura_Cliente.objects.values('estado').annotate(total=Sum('monto'))
        total_monto_proveedor = Factura_Proveedor.objects.values('estado').annotate(total=Sum('monto'))
        return Response({
            'total_monto_cliente': total_monto_cliente,
            'total_monto_proveedor': total_monto_proveedor
        })
    

class FacturasPorFechaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        if not fecha_inicio or not fecha_fin:
            return Response({'error': 'Debe proporcionar fecha_inicio y fecha_fin'}, status=400)
        
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')

        facturas_cliente = Factura_Cliente.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        facturas_proveedor = Factura_Proveedor.objects.filter(fecha__range=(fecha_inicio, fecha_fin))

        serializer_cliente = FacturaClienteSerializer(facturas_cliente, many=True)
        serializer_proveedor = FacturaProveedorSerializer(facturas_proveedor, many=True)

        return Response({
            'facturas_cliente': serializer_cliente.data,
            'facturas_proveedor': serializer_proveedor.data
        })
    


class TotalClientesProveedoresView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_clientes = Cliente.objects.count()
        total_proveedores = Proveedor.objects.count()
        return Response({
            'total_clientes': total_clientes,
            'total_proveedores': total_proveedores
        })
    


class TotalFacturasPorUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rol = request.query_params.get('rol', 'contador')
        usuarios = Usuario.objects.filter(rol=rol).annotate(
            total_facturas_cliente=Count('facturas_cliente', distinct=True),
            total_facturas_proveedor=Count('facturas_proveedor', distinct=True)
        )
        serializer = UsuarioFacturaSerializer(usuarios, many=True)
        return Response(serializer.data)
    



import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Factura_Cliente, Factura_Proveedor

class ExportarDatosExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tipo = request.query_params.get('tipo', 'cliente')
        if tipo == 'cliente':
            facturas = Factura_Cliente.objects.all().values()
        else:
            facturas = Factura_Proveedor.objects.all().values()

        df = pd.DataFrame(facturas)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=facturas_{tipo}.xlsx'
        df.to_excel(response, index=False)
        return response
    

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Factura_Cliente, Factura_Proveedor

class ExportarDatosPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tipo = request.query_params.get('tipo', 'cliente')
        if tipo == 'cliente':
            facturas = Factura_Cliente.objects.all()
        else:
            facturas = Factura_Proveedor.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=facturas_{tipo}.pdf'
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        y = height - 40
        for factura in facturas:
            p.drawString(30, y, str(factura))
            y -= 20
            if y < 40:
                p.showPage()
                y = height - 40

        p.save()
        return response
    



import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from .models import Factura_Cliente, Factura_Proveedor
from django.utils.datastructures import MultiValueDictKeyError
from django.utils import timezone
from django.db import IntegrityError

class ImportarFacturasCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            tipo = request.query_params.get('tipo', 'cliente')
            file = request.FILES['file']
        except MultiValueDictKeyError:
            return Response({'error': 'No se ha proporcionado el archivo'}, status=400)

        file_path = default_storage.save(file.name, file)
        df = pd.read_csv(file_path)

        if tipo == 'cliente':
            for _, row in df.iterrows():
                row_dict = row.to_dict()
                if 'fecha_vencimiento' in row_dict:
                    fecha_vencimiento = pd.to_datetime(row_dict['fecha_vencimiento'])
                    if fecha_vencimiento.tzinfo is None or fecha_vencimiento.tzinfo.utcoffset(fecha_vencimiento) is None:
                        row_dict['fecha_vencimiento'] = timezone.make_aware(fecha_vencimiento)
                try:
                    Factura_Cliente.objects.create(**row_dict)
                except IntegrityError:
                    continue
        else:
            for _, row in df.iterrows():
                row_dict = row.to_dict()
                if 'fecha_vencimiento' in row_dict:
                    fecha_vencimiento = pd.to_datetime(row_dict['fecha_vencimiento'])
                    if fecha_vencimiento.tzinfo is None or fecha_vencimiento.tzinfo.utcoffset(fecha_vencimiento) is None:
                        row_dict['fecha_vencimiento'] = timezone.make_aware(fecha_vencimiento)
                try:
                    Factura_Proveedor.objects.create(**row_dict)
                except IntegrityError:
                    continue

        return Response({'status': 'success'})

import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.files.storage import default_storage
from .models import Factura_Cliente, Factura_Proveedor

class ImportarFacturasExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tipo = request.query_params.get('tipo', 'cliente')
        file = request.FILES['file']
        file_path = default_storage.save(file.name, file)
        df = pd.read_excel(file_path)

        if tipo == 'cliente':
            for _, row in df.iterrows():
                Factura_Cliente.objects.create(**row.to_dict())
        else:
            for _, row in df.iterrows():
                Factura_Proveedor.objects.create(**row.to_dict())

        return Response({'status': 'success'})
    

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Factura_Cliente, Factura_Proveedor

class ExportarTodasFacturasPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tipo = request.query_params.get('tipo', 'cliente')
        if tipo == 'cliente':
            facturas = Factura_Cliente.objects.all()
        else:
            facturas = Factura_Proveedor.objects.all()

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=todas_facturas_{tipo}.pdf'
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        y = height - 40
        for factura in facturas:
            p.drawString(30, y, str(factura))
            y -= 20
            if y < 40:
                p.showPage()
                y = height - 40

        p.save()
        return response


import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Factura_Cliente, Factura_Proveedor

class ExportarTodasFacturasExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tipo = request.query_params.get('tipo', 'cliente')
        if tipo == 'cliente':
            facturas = Factura_Cliente.objects.all().values()
        else:
            facturas = Factura_Proveedor.objects.all().values()

        df = pd.DataFrame(facturas)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=todas_facturas_{tipo}.xlsx'
        df.to_excel(response, index=False)
        return response
    


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Factura_Cliente, Factura_Proveedor

class ExportarFacturaPDFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tipo = request.query_params.get('tipo', 'cliente')
        factura_id = request.query_params.get('id')
        if tipo == 'cliente':
            factura = Factura_Cliente.objects.get(id=factura_id)
        else:
            factura = Factura_Proveedor.objects.get(id=factura_id)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=factura_{tipo}_{factura_id}.pdf'
        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        y = height - 40
        p.drawString(30, y, str(factura))
        p.save()
        return response
    


import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from .models import Factura_Cliente, Factura_Proveedor

class ExportarFacturaExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tipo = request.query_params.get('tipo', 'cliente')
        factura_id = request.query_params.get('id')
        if tipo == 'cliente':
            factura = Factura_Cliente.objects.filter(id=factura_id).values()
        else:
            factura = Factura_Proveedor.objects.filter(id=factura_id).values()

        df = pd.DataFrame(factura)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=factura_{tipo}_{factura_id}.xlsx'
        df.to_excel(response, index=False)
        return response



class ActualizarEstadoFacturaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tipo = request.data.get('tipo', 'cliente')
        factura_id = request.data.get('id')
        nuevo_estado = request.data.get('estado')

        if tipo == 'cliente':
            factura = Factura_Cliente.objects.get(id=factura_id)
        else:
            factura = Factura_Proveedor.objects.get(id=factura_id)

        try:
            factura.actualizar_estado(nuevo_estado)
            return Response({'status': 'success', 'mensaje': 'Estado actualizado correctamente'})
        except ValueError as e:
            return Response({'status': 'error', 'mensaje': str(e)}, status=400)
        

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Factura_Cliente, Factura_Proveedor

class FacturasPerdiendoPlataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        facturas_cliente = Factura_Cliente.objects.filter(estado='pendiente').annotate(
            mes=TruncMonth('fecha')
        ).values('mes', 'estado').annotate(
            total=Sum('monto')
        ).order_by('mes')

        facturas_proveedor = Factura_Proveedor.objects.filter(estado='pendiente').annotate(
            mes=TruncMonth('fecha')
        ).values('mes', 'estado').annotate(
            total=Sum('monto')
        ).order_by('mes')

        return Response({
            'facturas_cliente': list(facturas_cliente),
            'facturas_proveedor': list(facturas_proveedor)
        })

class FacturasGanandoPlataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        facturas_cliente = Factura_Cliente.objects.filter(estado='pagada').annotate(
            mes=TruncMonth('fecha')
        ).values('mes', 'estado').annotate(
            total=Sum('monto')
        ).order_by('mes')

        facturas_proveedor = Factura_Proveedor.objects.filter(estado='pagada').annotate(
            mes=TruncMonth('fecha')
        ).values('mes', 'estado').annotate(
            total=Sum('monto')
        ).order_by('mes')

        return Response({
            'facturas_cliente': list(facturas_cliente),
            'facturas_proveedor': list(facturas_proveedor)
        })
    



from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UsuarioSerializer

SPECIAL_PASSWORD = '345612'

@api_view(['POST'])
def register_user(request):
    special_password = request.data.get('special_password')
    if special_password != SPECIAL_PASSWORD:
        return Response({'error': 'Contraseña especial incorrecta'}, status=status.HTTP_403_FORBIDDEN)

    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Factura_Cliente, Factura_Proveedor
from .serializers import FacturaClienteSerializer, FacturaProveedorSerializer

@api_view(['PUT', 'PATCH'])
def editar_factura_cliente(request, pk):
    try:
        factura = Factura_Cliente.objects.get(pk=pk)
    except Factura_Cliente.DoesNotExist:
        return Response({'error': 'Factura no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = FacturaClienteSerializer(factura, data=request.data)
    elif request.method == 'PATCH':
        serializer = FacturaClienteSerializer(factura, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def editar_factura_proveedor(request, pk):
    try:
        factura = Factura_Proveedor.objects.get(pk=pk)
    except Factura_Proveedor.DoesNotExist:
        return Response({'error': 'Factura no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = FacturaProveedorSerializer(factura, data=request.data)
    elif request.method == 'PATCH':
        serializer = FacturaProveedorSerializer(factura, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)