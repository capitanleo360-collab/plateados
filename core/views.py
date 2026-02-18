from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.shortcuts import render, redirect, get_object_or_404


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

        errors = {}
        if not name:
            errors['name'] = "el nombre es requerido"

        if not price:
            errors['price'] = "el precio es requerido"

        if not description:
            errors['description'] = "la descripcion es requerido"

        if not category:
            errors['category'] = "la categoria es requerida"

        if errors:
            categories = Category.objects.all()
            return render(request, self.template_name,{
                'categories': categories,
                'errors': errors,
            })

        new_product = Product.objects.create(
            name=name,
            price=price,
            description=description,
            imagen=image_file,
            category=category
        )



        return redirect('catalogo')

class ProductListView(View):
    template_name = 'core/catalogo.html'

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, self.template_name,{'products': products})



class ProductDetailView(View):
    template_name = 'core/product_details.html'

    def get(self,request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'p': product})


class ProductUpdateView(View):
    template_name = 'core/product_update.html'

    def get(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        categories = Category.objects.all()
        return render(request, self.template_name, {'product': product,'categories':categories} )

    
    def post(self,request, id, *args,**kwargs):
        product = get_object_or_404(Product, id=id)


        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description", "")
        category_id = request.POST.get("category")
        category = Category.objects.filter(id=category_id).first() if category_id else None
        new_image_file = request.FILES.get('image')

        if new_image_file:
            if product.imagen and product.imagen.name:
                product.imagen.delete(save=False)
            
            product.imagen = new_image_file

        

        product.price = price
        product.name = name
        product.description = description
        product.category = category
        product.save()


        return redirect('catalogo')

class ProductDeleteview(View):
    template_name = 'core/product_confirm_delete.html'

    def get(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'product': product})

    
    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        product.delete()

        return redirect('catalogo')

def index(request):
    return render(request, 'core/index.html')


def login(request):
    return render(request, 'core/login.html')

def registro(request):
    return render(request, 'core/registro.html')



def pedir(request):
    return render(request, 'core/pedir.html')

# Create your views here.


class OrderCreateView(View):
    template_name = 'core/pedido.html'

    def get(self, request, id,*args, **kwargs):
        product = get_object_or_404(Product, id=id)
        return render(request, self.template_name, {'product': product})

    
    def post(self, request, id, *args, **kwargs):
        current_user=request.user
        order_date = request.POST.get("order_date")
        order_time = request.POST.get("order_time")
        quantity = request.POST.get("quantity")
        product = Product.objects.filter(id=id).first() if id else None


        new_order = Order.objects.create(
            order_date=order_date,
            order_time=order_time,
            quantity=quantity,
            product=product,
            user=current_user

        )

        new_bill= Bill.objects.create(
            order=new_order

        )


        return redirect('pedir')
