from django.shortcuts import render, redirect
from django.views import View
from .models import *

class ProductCreateView(View):
    template_name = 'core/registro_de_producto.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description", "")

        category_id = request.POST.get("category")
        category = Category.objects.filter(id=category_id).first() if category_id else None

        image_file = request.FILES.get('image')
        print(image_file)

        new_product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            imagen=image_file,
            category=category
        )
        return redirect('catalogo')

def index(request):
    return render(request, 'core/index.html')

def catalogo(request):
    return render(request, 'core/catalogo.html')

def login(request):
    return render(request, 'core/login.html')

def registro(request):
    return render(request, 'core/registro.html')

def pedido(request):
    return render(request, 'core/pedido.html')





def pedir(request):
    return render(request, 'core/pedir.html')

# Create your views here.
