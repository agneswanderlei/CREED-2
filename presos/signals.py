from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Presos
from usuarios.models import AuditLog


@receiver(post_save, sender=Presos)
def log_presos_save(sender, instance, created, **kwargs):
    if created:
        print(instance.created_at)
        # Registro de criação
        AuditLog.objects.create(
            user=instance.modified_by,  # Assumindo que há um campo modified_by no modelo para capturar o usuário
            action="CREATE",
            description=f"Preso criado: {instance.name_full}",
        )
    else:
        user = instance.name_full
        print(f'update {user}')
        # Registro de atualização
        AuditLog.objects.create(
            user=instance.modified_by,
            action="UPDATE",
            description=f"Preso atualizado: {instance.name_full}",
        )


@receiver(post_delete, sender=Presos)
def log_presos_delete(sender, instance, **kwargs):
    # Registro de exclusão
    AuditLog.objects.create(
        user=instance.modified_by,
        action="DELETE",
        description=f"Preso excluído: {instance.name_full}",
    )