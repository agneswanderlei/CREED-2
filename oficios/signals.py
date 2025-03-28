import os
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Oficios

@receiver(post_delete, sender=Oficios)
def delete_file_on_delete(sender, instance, **kwargs):
    if instance.anexos:
        if os.path.isfile(instance.anexos.path):
            os.remove(instance.anexos.path)  # Exclui o arquivo físico