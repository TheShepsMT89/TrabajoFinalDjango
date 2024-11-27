from rest_framework.permissions import BasePermission


class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == "admin"


class EsContador(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == "contador"


class EsGerente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == "gerente"
