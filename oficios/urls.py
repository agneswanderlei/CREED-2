from django.urls import path
from . import views

urlpatterns = [
    path('oficios/list/', views.OficiosList.as_view(), name='oficios_list'),
    path('oficios/add/', views.OficiosCreate.as_view(), name='oficios_add'),
    path('oficios/<int:pk>/detail/', views.OficiosDetail.as_view(),
         name='oficios_detail'),
    path('oficios/<int:pk>/update/', views.OficiosUpdate.as_view(),
         name='oficios_update'),
    path('oficios/<int:pk>/delete/', views.OficiosDelete.as_view(),
         name='oficios_delete'),
    path('relatorios/pdf/', views.gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
]

htmlx_urlpatterns = [
    
]

urlpatterns += htmlx_urlpatterns