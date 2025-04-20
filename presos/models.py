from django.db import models
from django.conf import settings


class Tipo_documento(models.Model):
    tipos = models.CharField(max_length=100)

    class Meta:
        ordering = ['tipos']

    def __str__(self):
        return self.tipos


class States(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class PostGrad(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Presos(models.Model):

    number_doc = models.CharField(max_length=100, primary_key=True)
    type_doc = models.ForeignKey(
        Tipo_documento,
        on_delete=models.PROTECT,
        related_name='tipos_docs'
    )
    name_full = models.CharField(max_length=200)
    state_origin = models.ForeignKey(
        States,
        on_delete=models.PROTECT,
        related_name='states'
    )
    institutions = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        related_name='institutions'
    )
    posto_grad = models.ForeignKey(
        PostGrad,
        on_delete=models.PROTECT,
        related_name='postgrad'
    )
    sector = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='presos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        ordering = ['name_full']

    def __str__(self):
        return f'{self.number_doc} - {self.name_full}'


class Teste(models.Model):
    n_pront = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    
    
    def __str__(self):
        return self.name