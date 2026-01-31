from django.shortcuts import render




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
