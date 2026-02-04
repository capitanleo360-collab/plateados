from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.index, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('pedido/', views.pedido, name='pedido'),
    path('pedir/', views.pedir, name='pedir'),
    path('registro_de_producto/', ProductCreateView.as_view(), name='registro_de_producto'),
]