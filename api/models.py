from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    User,
)
from django.utils import timezone
from django.conf import settings


class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user = self.model(email=email, nombre=nombre, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nombre, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, nombre, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    ROL_CHOICES = [
        ("admin", "Admin"),
        ("contador", "Contador"),
        ("gerente", "Gerente"),
    ]

    id = models.BigAutoField(primary_key=True)
    nombre = models.TextField(null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=128)
    rol = models.CharField(max_length=10, choices=ROL_CHOICES, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    creado_en = models.DateTimeField(default=timezone.now)
    avatar = models.URLField(null=True, blank=True)  # Cambiar a URLField
    telefono = models.TextField(blank=True, null=True)  # Nuevo campo
    direccion = models.TextField(blank=True, null=True)  # Nuevo campo

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombre"]

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    nombre = models.TextField(null=False)
    email = models.EmailField(unique=True, null=False)
    telefono = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="clientes",
    )  # Asegúrate de tener este campo

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre = models.TextField(null=False)
    email = models.EmailField(unique=True, null=False)
    telefono = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="proveedores",
    )  # Asegúrate de tener este campo

    def __str__(self):
        return self.nombre


class Factura_Cliente(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("pagada", "Pagada"),
        ("cancelada", "Cancelada"),
    ]

    id = models.BigAutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.SET_NULL, null=True, related_name="facturas_cliente"
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name="facturas_cliente"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, null=False)
    descripcion = models.TextField(blank=True, null=True)
    numero_factura = models.TextField(unique=True, null=False)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    accion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_factura} - {self.estado}"


class Factura_Proveedor(models.Model):
    ESTADO_CHOICES = [
        ("pendiente", "Pendiente"),
        ("pagada", "Pagada"),
        ("cancelada", "Cancelada"),
    ]

    id = models.BigAutoField(primary_key=True)
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="facturas_proveedor",
    )
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, related_name="facturas_proveedor"
    )
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, null=False)
    descripcion = models.TextField(blank=True, null=True)
    numero_factura = models.TextField(unique=True, null=False)
    fecha_vencimiento = models.DateTimeField(blank=True, null=True)
    accion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_factura} - {self.estado}"

    def actualizar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADO_CHOICES):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError("Estado no válido")


from django.conf import settings


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Cambia auth.User por settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
    )
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"

    def actualizar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADO_CHOICES):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError("Estado no válido")


from django.conf import settings


class ReporteFactura(models.Model):
    id = models.BigAutoField(primary_key=True)
    numero_factura = models.CharField(max_length=255, unique=True)
    cliente = models.CharField(max_length=255, null=True, blank=True)
    proveedor = models.CharField(max_length=255, null=True, blank=True)
    fecha = models.DateTimeField()
    fecha_vencimiento = models.DateTimeField()

    accion = models.BooleanField(default=False)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True
    )
    timestamp_accion = models.DateTimeField(auto_now=True)
    motivo_accion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reporte de Factura {self.numero_factura}"


from django.db import models
from django.conf import settings


class SimpleMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.user.nombre}: {self.content[:20]}"
