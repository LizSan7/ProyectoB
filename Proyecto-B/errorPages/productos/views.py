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

import json
#Función que agrega un producto con un objeto JSON
def registrar_producto(request):
    #Checa si muestra request es de tipo POST
    if request.method == 'POST':
        #quiere decir que si estoy manejando el request
        try:
            data = json.loads(request.body) #Parametro es un texto que debería ser un JSON
            producto = Producto.objects.create(
                nombre = data['nombre'],
                precio = data['precio'],
                imagen = data['imagen']
            ) #Create directamente mete el objeto en la BD
            return JsonResponse(
                {
                    'mensaje': 'Registro exitoso',
                    'id': producto.id    
                }, status=201
            )
        except Exception as e:
            print(str(e))
            return JsonResponse(
                {'error': str(e)}, status = 400
            )
    #Si no es POST el request...
    return JsonResponse (
        {'error': 'El método no es soportado'}, status = 405
    )

from django.shortcuts import get_object_or_404
#Funciones para el método PUT
def actualizar_producto(request, id_producto):
    if request.method == 'PUT':
        producto = get_object_or_404(Producto, id= id_producto)
        try:
            #La información de la modificación del producto viene del body del request
            data = json.loads(request.body)
            producto.nombre = data.get('nombre', producto.nombre)
            producto.precio = data.get('precio', producto.precio)
            producto.imagen = data.get('imagen', producto.imagen)
            producto.save()
            return JsonResponse({'mensaje': 'Producto actualizado correctamente'}, status =200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Método no es PUT'}, status=405)
#Funciones para DELETE

#Función adicional para GET
#De retornar un producto especifico