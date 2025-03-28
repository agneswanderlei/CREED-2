from django.urls import path
from . import views

urlpatterns = [
    path('presos/list/', views.PresosList.as_view(), name='presos_list'),
    path('presos/add/', views.PresosCreate.as_view(), name='presos_add'),
    path('presos/<str:pk>/detail/', views.PresosDetail.as_view(),
         name='presos_detail'),
    path('presos/<str:pk>/update/', views.PresosUpdate.as_view(),
         name='presos_update'),
    path('presos/<str:pk>/delete/', views.PresosDelete.as_view(),
         name='presos_delete'),

]