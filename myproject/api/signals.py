from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AuditLog, FacturaCliente, FacturaProveedor

@receiver(post_save, sender=FacturaCliente)
def log_factura_cliente_action(sender, instance, created, **kwargs):
    if created:
        action = "FacturaCliente creada"
    else:
        action = "FacturaCliente actualizada"
    AuditLog.objects.create(user=instance.usuario, action=action, details=f"FacturaCliente ID: {instance.id}")

@receiver(post_delete, sender=FacturaCliente)
def log_factura_cliente_delete(sender, instance, **kwargs):
    AuditLog.objects.create(user=instance.usuario, action="FacturaCliente eliminada", details=f"FacturaCliente ID: {instance.id}")

@receiver(post_save, sender=FacturaProveedor)
def log_factura_proveedor_action(sender, instance, created, **kwargs):
    if created:
        action = "FacturaProveedor creada"
    else:
        action = "FacturaProveedor actualizada"
    AuditLog.objects.create(user=instance.usuario, action=action, details=f"FacturaProveedor ID: {instance.id}")

@receiver(post_delete, sender=FacturaProveedor)
def log_factura_proveedor_delete(sender, instance, **kwargs):
    AuditLog.objects.create(user=instance.usuario, action="FacturaProveedor eliminada", details=f"FacturaProveedor ID: {instance.id}")