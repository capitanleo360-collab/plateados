from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100,blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    Created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    REQUIRED_FIELDS = ["phone_number"]
    class Meta:
        db_table = "users"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"


    def __str__(self):
        return f"{self.username} ({self.email})"
    


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(unique=True, max_length=15, blank=True, null=True)
    correo = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'cliente'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Detallepedido(models.Model):
    pk = models.CompositePrimaryKey('pedido_id', 'producto_id')
    pedido = models.ForeignKey('Pedido', models.DO_NOTHING)
    producto = models.ForeignKey('Producto', models.DO_NOTHING)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detallepedido'
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedidos"
    
    def __str__(self):
        return f"Pedido ID: {self.pedido.id}, Producto: {self.producto.nombre}, Cantidad: {self.cantidad}"


class Factura(models.Model):
    fecha = models.DateField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pedido = models.OneToOneField('Pedido', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'factura'
        vebose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura ID: {self.id}, Total: {self.total}"


class Mesa(models.Model):
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=20)
    estado = models.IntegerField()
    mesero = models.ForeignKey('Mesero', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'mesa'
        vebose_name = "Mesa"
        verbose_name_plural = "Mesas"
    
    def __str__(self):
        return f"Mesa ID: {self.id}, Ubicación: {self.ubicacion}, Capacidad: {self.capacidad}"


class Mesero(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    puesto = models.CharField(max_length=20)
    salario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'mesero'
        vebose_name = "Mesero"
        verbose_name_plural = "Meseros"
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Pedido(models.Model):
    fecha_hora = models.DateTimeField()
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    mesa = models.ForeignKey(Mesa, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pedido'
        vebose_name = "Pedido"
        verbose_name_plural = "Pedidos"
    
    def __str__(self):
        return f"Pedido ID: {self.id}, Cliente: {self.cliente.nombre} {self.cliente.apellido}, Mesa ID: {self.mesa.id}"


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'producto'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"



# Create your models here.
