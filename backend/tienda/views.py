from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Categoria, Producto  # <--- ESTA LÍNEA ES VITAL
from .serializers import CategoriaSerializer, ProductoSerializer

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all() # <- DEVOLVEMOS ESTA LÍNEA PARA QUE NO HAYA ERROR
    serializer_class = ProductoSerializer

    def get_queryset(self):
        queryset = Producto.objects.all()
        categoria_id = self.request.query_params.get('categoria')
        if categoria_id is not None:
            queryset = queryset.filter(categoria_id=categoria_id)
        return queryset

@api_view(['POST'])
def procesar_pago(request):
    items = request.data.get('items', [])
    
    if not items:
        return Response({'error': 'El carrito está vacío'}, status=400)

    total = 0
    productos_a_actualizar = []

    # 1. Verificar stock y calcular total
    for item in items:
        prod = get_object_or_404(Producto, id=item['id'])
        if prod.stock < item['cantidad']:
            return Response({'error': f'Sin stock suficiente para {prod.nombre}'}, status=400)
        
        subtotal = prod.precio * item['cantidad']
        total += subtotal
        productos_a_actualizar.append((prod, item['cantidad']))

    pago_exitoso = True 

    if pago_exitoso:
        for prod, cantidad in productos_a_actualizar:
            prod.stock -= cantidad
            prod.save()
        
        return Response({
            'status': 'success',
            'message': 'Pago procesado correctamente con Izipay',
            'total': total
        })
    else:
        return Response({'error': 'El pago fue rechazado por la pasarela'}, status=400)