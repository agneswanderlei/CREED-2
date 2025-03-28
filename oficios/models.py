from django.db import models
from presos.models import Presos
from django.core.validators import FileExtensionValidator







class Situacao(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Oficios(models.Model):

    TIPO_PRISAO = (
        ('ABERTA', 'Aberta'),
        ('FECHADA', 'fechada'),
        ('SEMIABERTA', 'Semiaberta'),
        ('HARMONIZADA', 'Harmonizada'),
        ('PREVENTIVA', 'Preventiva'),
        ('TEMPORARIA', 'Temporária'),
        ('OUTROS', 'Outros')

    )
    n_pront_presos = models.ManyToManyField(Presos, related_name='oficioss')
    n_oficios = models.CharField(max_length=100,)
    n_sei = models.CharField(max_length=50,)
    orgao = models.CharField(max_length=50,)
    date_send = models.DateField()
    descricao = models.TextField()
    tipo_prisao = models.CharField(
        max_length=50,
        choices=TIPO_PRISAO,
        null=False,
        blank=False
    )
    anexos = models.FileField(
        upload_to='documentos/',  # Diretório para salvar os arquivos
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],  # Validação de extensões
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.n_oficios


class OficiosPresos(models.Model):
    n_oficios = models.ForeignKey(
        Oficios,
        on_delete=models.PROTECT,
        related_name='rel_oficio'
    )
    prontuario = models.ForeignKey(
        Presos,
        on_delete=models.PROTECT,
        related_name='rel_presos'
    )

    def __str__(self):
        return self.n_oficios
