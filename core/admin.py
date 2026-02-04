from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Category, Product, Order, Bill

admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Bill)
# Register your models here.
