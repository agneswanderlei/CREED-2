from django.urls import path
from . import views

urlpatterns = [
    path('relatorios/', views.relatoriohome, name='relatorio'),
    path('relatorios/detail/', views.relatorio_detail, name='relatorio_detail'),

    
]