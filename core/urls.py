from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.index, name='inicio'),
    path('catalogo/', ProductListView.as_view(), name='catalogo'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('registro/', views.registro, name='registro'),
    path('pedido/<int:id>/', OrderCreateView.as_view(),name='pedido'),
    path('pedir/', views.pedir, name='pedir'),
    path('registro_de_producto/', ProductCreateView.as_view(), name='registro_de_producto'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:id>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:id>/delete/', ProductDeleteview.as_view(), name='product_delete'),
    

]