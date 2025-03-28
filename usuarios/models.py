from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    codigo_usuario = models.CharField(max_length=100, blank=True, null=True, default=None)  # Campo adicional
