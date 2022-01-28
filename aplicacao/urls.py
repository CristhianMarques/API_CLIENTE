from django.urls import path

from . import views


urlpatterns = [
    #path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('parametro/', views.parametro, name='parametro'),
    path('contato/', views.contato, name='contato'),
    path('eventos/', views.eventos, name='eventos'),
    path('ProcessaEventosManual/', views.Processa_Eventos_Manual, name='ProcessaEventos'),
]
