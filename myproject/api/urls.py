from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacturaClienteViewSet, FacturaProveedorViewSet, ClienteViewSet, ProveedorViewSet, LoginView, LogoutView, VistaSoloAdmin, UsuarioLogueadoView, AuditLogListView, ReporteFacturaViewSet, SimpleMessageViewSet

# Crear el router
router = DefaultRouter()
router.register('facturas-clientes', FacturaClienteViewSet, basename='facturas-clientes')
router.register('facturas-proveedores', FacturaProveedorViewSet, basename='facturas-proveedores')
router.register('clientes', ClienteViewSet, basename='clientes')
router.register('proveedores', ProveedorViewSet, basename='proveedores')
router.register('reportes-facturas', ReporteFacturaViewSet, basename='reportes-facturas')
router.register('simple-messages', SimpleMessageViewSet, basename='simple-messages')

# Definir las rutas
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-only/', VistaSoloAdmin.as_view(), name='admin_only'),
    path('usuario-logueado/', UsuarioLogueadoView.as_view(), name='usuario_logueado'),
    path('audit-logs/', AuditLogListView.as_view(), name='audit_logs'),  # Registrar la vista de registros de auditoría
]