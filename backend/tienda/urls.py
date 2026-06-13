from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, procesar_pago # <--- AQUÍ IMPORTAMOS procesar_pago

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pagar/', procesar_pago), 
]