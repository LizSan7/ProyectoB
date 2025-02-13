from django.shortcuts import render, redirect
from .models import Producto
#Este Objeto me permite enviar respuesta JSON
from django.http import JsonResponse

# from .forms import productoForm
#ya
# Create your views here.


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