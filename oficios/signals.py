import os
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Oficios
from usuarios.models import AuditLog


@receiver(post_save, sender=Oficios)
def log_oficios_save(sender, instance, created, **kwargs):
    if created:
        # Registro da Criação
        AuditLog.objects.create(
            user=instance.modified_by,
            action='CREATE',
            description=f'Oficio criado: Nº {instance.n_oficios}'
        )
    else:
        # Registro de atualização
        AuditLog.objects.create(
            user=instance.modified_by,
            action='UPDATE',
            description=f'Ofício atualizado: Nº {instance.n_oficios}'
        )


@receiver(post_delete, sender=Oficios)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.anexos:
        if os.path.isfile(instance.anexos.path):
            os.remove(instance.anexos.path)  # Exclui o arquivo físico


@receiver(post_delete, sender=Oficios)
def log_oficios_delete(sender, instance, **kargs):
    # Registro de exclusao
    AuditLog.objects.create(
        user=instance.modified_by,
        action='DELETE',
        description=f'Oficio deletado: Nº {instance.n_oficios}'
    )
