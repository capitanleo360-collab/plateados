from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date


class ProductCreateView(LoginRequiredMixin, View):
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
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        products = Product.objects.all()

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()

        paginator = Paginator(products, self.paginate_by)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'products': page_obj.object_list,
            'query': query,
        }

        return render(request, self.template_name, context)


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



# Create your views here.


class OrderCreateView(LoginRequiredMixin, View):
    template_name = 'core/pedido.html'

    def get(self, request, id,*args, **kwargs):
        product = get_object_or_404(Product, id=id)
        today = date.today().strftime('%Y-%m-%d')
        return render(request, self.template_name, {'product': product, 'today': today})

    
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


        return redirect('pedir' , id=new_order.id)
    

class OrderUpdateView(View):
    template_name = 'core/pedir.html'

    def get(self, request, id,*args, **kwargs):
        order = get_object_or_404(Order, id=id)
        return render(request, self.template_name, {'order': order})

    
    def post(self, request, id, *args, **kwargs):
        bank = request.POST.get("metodo_pago")
        reference = request.POST.get("reference")

        bill= get_object_or_404(Bill, order__id=id)
        bill.bank = bank
        bill.reference = reference
        bill.payment= True
        bill.save()

        return redirect('catalogo')
    
class OrderListView(View):
    template_name = 'core/compras.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        current_user=request.user
        orders = Order.objects.filter(user=current_user)
        if query:
            orders = orders.filter(
                Q(product__name__icontains=query)|
                Q(total__icontains=query)
            ).distinct()

        paginator = Paginator(orders, self.paginate_by)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'orders': page_obj.object_list,
            'query': query,
        }

        return render(request, self.template_name, context)
    

class UserLoginView(View):
    template_name = 'core/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('inicio')
        
        form = LoginForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('inicio')
        
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                
                login(request, user)
                return redirect('inicio')
            else:
                return render(request, self.template_name, {
                    'form': form,
                    'error': 'Credenciales inválidas. Por favor, inténtalo de nuevo.'
                })
        return render(request, self.template_name, {'form': form})
    

class UserRegisterView(View):
    template_name = 'core/registro.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('inicio')
        
        form = RegisterForm()
        print(form)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('inicio')
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password = form.cleaned_data['password2']
            
            User = get_user_model()
            user = User.objects.create_user(username=username, email=email, password=password)

            login(request, user)
            return redirect('inicio')
        
        return render(request, self.template_name, {'form': form})

class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class OrderDeleteView(View):
    template_name = 'core/order_confirm_delete.html'

    def get(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, id=id)
        return render(request, self.template_name, {'order': order})

    
    def post(self, request, id, *args, **kwargs):
        order = get_object_or_404(Order, id=id)
        order.bill.delete()
        order.delete()

        return redirect('inicio')
    

class AllOrdersListView(View):
    template_name = 'core/todas_compras.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        orders = Order.objects.all()
        print(orders)
        if query:
            orders = orders.filter(
                Q(product__name__icontains=query)|
                Q(user__username__icontains=query)|
                Q(total__icontains=query)
            ).distinct()

        paginator = Paginator(orders, self.paginate_by)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'orders': page_obj.object_list,
            'query': query,
        }

        return render(request, self.template_name, context)