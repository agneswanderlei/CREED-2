from django.utils.formats import number_format
from presos.models import Presos


def get_presos_metrics():
    presos = Presos.objects.all().count()