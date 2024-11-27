from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import FacturaClienteViewSet, FacturaProveedorViewSet, ClienteViewSet, ProveedorViewSet, LoginView, LogoutView, VistaSoloAdmin, UsuarioLogueadoView, AuditLogListView, ReporteFacturaViewSet, SimpleMessageViewSet, TotalPorCobrarView, TotalPorPagarView, FacturasVencidasView, ProyeccionFlujoCajaView, NotificacionesFacturasView,TotalFacturasPorUsuarioView,TotalFacturasPorEstadoView, TotalMontoPorEstadoView, FacturasPorFechaView, TotalClientesProveedoresView,  ExportarDatosExcelView, ExportarDatosPDFView, ImportarFacturasCSVView, ImportarFacturasExcelView,ExportarFacturaExcelView, ExportarFacturaPDFView, ExportarTodasFacturasExcelView, ExportarTodasFacturasPDFView


from .views import (
    FacturaClienteViewSet, FacturaProveedorViewSet, ClienteViewSet, ProveedorViewSet,
    LoginView, LogoutView, VistaSoloAdmin, UsuarioLogueadoView, AuditLogListView,
    ReporteFacturaViewSet, SimpleMessageViewSet, TotalPorCobrarView, TotalPorPagarView,
    FacturasVencidasView, ProyeccionFlujoCajaView, NotificacionesFacturasView,
    TotalFacturasPorUsuarioView, TotalFacturasPorEstadoView, TotalMontoPorEstadoView,
    FacturasPorFechaView, TotalClientesProveedoresView, UsuarioAdminViewSet, 
    ClienteAdminViewSet, ProveedorAdminViewSet, FacturaClienteAdminViewSet, ActualizarEstadoFacturaView,
    FacturaProveedorAdminViewSet
)

# Crear el router
router = DefaultRouter()
router.register('facturas-clientes', FacturaClienteViewSet, basename='facturas-clientes')
router.register('facturas-proveedores', FacturaProveedorViewSet, basename='facturas-proveedores')
router.register('clientes', ClienteViewSet, basename='clientes')
router.register('proveedores', ProveedorViewSet, basename='proveedores')
router.register('reportes-facturas', ReporteFacturaViewSet, basename='reportes-facturas')
router.register('simple-messages', SimpleMessageViewSet, basename='simple-messages')
router.register('admin/usuarios', UsuarioAdminViewSet, basename='admin-usuarios')
router.register('admin/clientes', ClienteAdminViewSet, basename='admin-clientes')
router.register('admin/proveedores', ProveedorAdminViewSet, basename='admin-proveedores')
router.register('admin/facturas-clientes', FacturaClienteAdminViewSet, basename='admin-facturas-clientes')
router.register('admin/facturas-proveedores', FacturaProveedorAdminViewSet, basename='admin-facturas-proveedores')

# Definir las rutas
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-only/', VistaSoloAdmin.as_view(), name='admin_only'),
    path('usuario-logueado/', UsuarioLogueadoView.as_view(), name='usuario_logueado'),
    path('audit-logs/', AuditLogListView.as_view(), name='audit_logs'),  # Registrar la vista de registros de auditoría
    path('total-por-cobrar/', TotalPorCobrarView.as_view(), name='total_por_cobrar'),  # Registrar la vista de total por cobrar
    path('total-por-pagar/', TotalPorPagarView.as_view(), name='total_por_pagar'),  # Registrar la vista de total por pagar
    path('facturas-vencidas/', FacturasVencidasView.as_view(), name='facturas_vencidas'),  # Registrar la vista de facturas vencidas
    path('proyeccion-flujo-caja/', ProyeccionFlujoCajaView.as_view(), name='proyeccion_flujo_caja'),  # Registrar la vista de proyección de flujo de caja
    
    path('notificaciones-facturas/', NotificacionesFacturasView.as_view(), name='notificaciones_facturas'),
    path('total-facturas-por-usuario/', TotalFacturasPorUsuarioView.as_view(), name='total_facturas_por_usuario'),
    path('total-facturas-por-estado/', TotalFacturasPorEstadoView.as_view(), name='total_facturas_por_estado'),
    path('total-monto-por-estado/', TotalMontoPorEstadoView.as_view(), name='total_monto_por_estado'),
    path('facturas-por-fecha/', FacturasPorFechaView.as_view(), name='facturas_por_fecha'),
    path('total-clientes-proveedores/', TotalClientesProveedoresView.as_view(), name='total_clientes_proveedores'),
     path('actualizar-estado-factura/', ActualizarEstadoFacturaView.as_view(), name='actualizar_estado_factura'),
    path('exportar-datos-excel/', ExportarDatosExcelView.as_view(), name='exportar_datos_excel'),
    path('exportar-datos-pdf/', ExportarDatosPDFView.as_view(), name='exportar_datos_pdf'),
    path('importar-facturas-csv/', ImportarFacturasCSVView.as_view(), name='importar_facturas_csv'),
    path('importar-facturas-excel/', ImportarFacturasExcelView.as_view(), name='importar_facturas_excel'),
     path('exportar-factura-excel/', ExportarFacturaExcelView.as_view(), name='exportar_factura_excel'),
    path('exportar-factura-pdf/', ExportarFacturaPDFView.as_view(), name='exportar_factura_pdf'),
    path('exportar-todas-facturas-excel/', ExportarTodasFacturasExcelView.as_view(), name='exportar_todas_facturas_excel'),
    path('exportar-todas-facturas-pdf/', ExportarTodasFacturasPDFView.as_view(), name='exportar_todas_facturas_pdf'),





]