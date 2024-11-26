from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Factura_Cliente, Factura_Proveedor, Cliente, Proveedor, AuditLog

@receiver(post_save, sender=Factura_Cliente)
def audit_factura_cliente_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    if instance.usuario:
        AuditLog.objects.create(
            user=instance.usuario,
            action=f'Factura_Cliente {action}',
            details=f'Factura_Cliente {instance.id} - {action}',
        )

@receiver(post_delete, sender=Factura_Cliente)
def audit_factura_cliente_delete(sender, instance, **kwargs):
    if instance.usuario:
        AuditLog.objects.create(
            user=instance.usuario,
            action='deleted',
            details=f'Factura_Cliente {instance.id} - deleted',
        )

@receiver(post_save, sender=Factura_Proveedor)
def audit_factura_proveedor_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    if instance.usuario:
        AuditLog.objects.create(
            user=instance.usuario,
            action=f'Factura_Proveedor {action}',
            details=f'Factura_Proveedor {instance.id} - {action}',
        )

@receiver(post_delete, sender=Factura_Proveedor)
def audit_factura_proveedor_delete(sender, instance, **kwargs):
    if instance.usuario:
        AuditLog.objects.create(
            user=instance.usuario,
            action='deleted',
            details=f'Factura_Proveedor {instance.id} - deleted',
        )

@receiver(post_save, sender=Cliente)
def audit_cliente_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    if instance.creado_por:
        AuditLog.objects.create(
            user=instance.creado_por,
            action=f'Cliente {action}',
            details=f'Cliente {instance.id} - {action}',
        )

@receiver(post_delete, sender=Cliente)
def audit_cliente_delete(sender, instance, **kwargs):
    if instance.creado_por:
        AuditLog.objects.create(
            user=instance.creado_por,
            action='deleted',
            details=f'Cliente {instance.id} - deleted',
        )

@receiver(post_save, sender=Proveedor)
def audit_proveedor_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    if instance.creado_por:
        AuditLog.objects.create(
            user=instance.creado_por,
            action=f'Proveedor {action}',
            details=f'Proveedor {instance.id} - {action}',
        )

@receiver(post_delete, sender=Proveedor)
def audit_proveedor_delete(sender, instance, **kwargs):
    if instance.creado_por:
        AuditLog.objects.create(
            user=instance.creado_por,
            action='deleted',
            details=f'Proveedor {instance.id} - deleted',
        )