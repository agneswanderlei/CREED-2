from django.urls import path
from . import views

urlpatterns = [
    path('relatorios/', views.relatoriohome, name='relatorio'),
    path('relatorios/detail/', views.relatorio_detail, name='relatorio_detail'),
    path("get-oficios/", views.get_oficios, name="get_oficios"),
    path("gerar-pdf/", views.gerar_pdf, name="gerar_pdf"),

]
