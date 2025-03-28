from django.urls import path
from . import views

urlpatterns = [
    path('relatorios/', views.relatoriohome, name='relatorio'),
    path('relatorio/detail/', views.RelatorioList.as_view(), name='presos_detail'),
]
