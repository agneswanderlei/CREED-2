from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    codigo_usuario = models.CharField(max_length=100, blank=True, null=True, default=None)  # Campo adicional


class AuditLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Configura a relação com o modelo de usuário
        on_delete=models.SET_NULL,  # Define o que acontece se o usuário for deletado
        null=True,  # Permite que o campo seja nulo
        blank=True  # Permite que o campo seja deixado em branco
    )
    action = models.CharField(max_length=50)  # Exemplo: "CREATE", "UPDATE", "DELETE"
    description = models.TextField()  # Detalhes da ação realizada
    timestamp = models.DateTimeField(auto_now_add=True)  # Data e hora da ação

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"