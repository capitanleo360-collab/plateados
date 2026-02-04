from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator

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

class Category(models.Model):
    name = models.CharField(verbose_name='Nombre', max_length= 100)
    description = models.TextField(
        verbose_name='Descripcion detallada',
        max_length=400,
        blank=True,
        null= True
    )
    class Meta:
        db_table = "categories"
        verbose_name = "categoria"
        verbose_name_plural = "categorias"

    def str(self):
        return

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, models.PROTECT)
    imagen = models.ImageField(
        verbose_name='imagen',
        upload_to = 'core/Product/',
        validators= [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png','webp'])],
        blank = True,
        null = True
    )
    description = models.TextField(
        verbose_name='Descripcion detallada',
        max_length=400,
        blank=True,
        null= True
    )

    class Meta:
        db_table = 'products'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.name} - ${self.price}"

class Order(models.Model):

    order_date = models.DateField()
    order_time = models.TimeField() 
    user = models.ForeignKey(User, models.PROTECT)
    product = models.ForeignKey(Product, models.PROTECT)
    total = models.DecimalField(decimal_places= 2, max_digits=10)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.total = self.product.price * self.quantity
        super().save(*args, **kwargs)    

    class Meta:
        db_table = 'orders'
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
    
    def __str__(self):
        return f"Pedido ID: #{self.id}, Cliente: {self.user.first_name} {self.user.first_name}"

class Bill(models.Model):
    order = models.OneToOneField(Order, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment = models.BooleanField(default=False)
    reference = models.CharField(max_length=16)
    bank = models.CharField(max_length=20)

    class Meta:
        db_table = 'bills'
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura ID: {self.id}, Total: {self.order.total}"



# Create your models here.
