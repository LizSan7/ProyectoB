from django.urls import path
from . views import *

urlpatterns= [
    path('api/get', lista_productos, name='lista')
]