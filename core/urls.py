from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='inicio'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
]