from django.shortcuts import render, redirect
from .models import Producto
#Este Objeto me permite enviar respuesta JSON
from django.http import JsonResponse

from .forms import productoForm

# Create your views here.

#Una vista que cargue y maneje al mismo tiempo el formulario
def agregar_producto(request):
    #checar si vengo del formulario
    if request.method == 'POST':
        #Quiere decir que enviaron el form
        form = productoForm(request.POST)
        #Checar que sus datos estén bien
        if form.is_valid():
            #lo guardo en bd
            form.save()
            return redirect('ver')
        #Que pasa si no fue que mandaron el form
    else:
            form = productoForm
    return render(request, 'agregar.html',{'form': form})

#Vista que devuelve los productos como json
def lista_productos(request):
    #Obtener todos los objetos de productos de la bd
    productos = Producto.objects.all()
    
    #Vamos a guardar los datos en un diccionario
    #Este diccionario fue creado al aire y no es seguro
    data = [
        {
            'nombre': p.nombre,
            'precio': p.precio,
            'imagen': p.imagen
        }
        for p in productos
    ]
    return JsonResponse(data, safe=False)

def ver_productos(request):
    return render(request, 'ver.html')