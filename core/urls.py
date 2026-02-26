from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('', views.index, name='inicio'),
    path('catalogo/', ProductListView.as_view(), name='catalogo'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('registro/', UserRegisterView.as_view(), name='registro'),
    path('pedido/<int:id>/', OrderCreateView.as_view(),name='pedido'),
    path('pedir/<int:id>/', OrderUpdateView.as_view(), name='pedir'),
    path('registro_de_producto/', ProductCreateView.as_view(), name='registro_de_producto'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:id>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:id>/delete/', ProductDeleteview.as_view(), name='product_delete'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('mis-compras/', OrderListView.as_view(), name='mis_compras'),
    path('order/<int:id>/delete/', OrderDeleteView.as_view(), name='order_delete'),
    path('todas-las-compras/', AllOrdersListView.as_view(), name='todas_las_compras'),
    

]