from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacturaClienteViewSet, FacturaProveedorViewSet, LoginView, LogoutView, VistaSoloAdmin

# Crear el router
router = DefaultRouter()
router.register('facturas-clientes', FacturaClienteViewSet, basename='facturas-clientes')
router.register('facturas-proveedores', FacturaProveedorViewSet, basename='facturas-proveedores')

# Definir las rutas
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin-only/', VistaSoloAdmin.as_view(), name='admin_only'),
]