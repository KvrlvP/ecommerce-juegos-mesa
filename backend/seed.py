import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User
from tienda.models import Categoria, Producto

# 1. Crear Admin
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
    print("✅ Admin creado")
else:
    print("ℹ️ Admin ya existe")

# 2. Crear datos si está vacío
if Categoria.objects.count() == 0:
    print("Llenando base de datos...")
    c1 = Categoria.objects.create(nombre="Eurogames", descripcion="Estrategia")
    c2 = Categoria.objects.create(nombre="Party Games", descripcion="Fiestas")
    c3 = Categoria.objects.create(nombre="Juegos de Cartas", descripcion="Cartas")
    c4 = Categoria.objects.create(nombre="Juegos Cooperativos", descripcion="Coop")
    c5 = Categoria.objects.create(nombre="Juegos Familiares", descripcion="Familia")

    datos = [
        {"nombre":"Catan","precio":150,"stock":8,"categoria":c1,"imagen":"https://picsum.photos/400/300?random=1","descripcion":"Comercio"},
        {"nombre":"Terraforming Mars","precio":220,"stock":5,"categoria":c1,"imagen":"https://picsum.photos/400/300?random=2","descripcion":"Marte"},
        {"nombre":"Scythe","precio":280,"stock":3,"categoria":c1,"imagen":"https://picsum.photos/400/300?random=3","descripcion":"1920"},
        {"nombre":"Agricola","precio":180,"stock":6,"categoria":c1,"imagen":"https://picsum.photos/400/300?random=4","descripcion":"Granjas"},
        {"nombre":"Wingspan","precio":240,"stock":6,"categoria":c1,"imagen":"https://picsum.photos/400/300?random=5","descripcion":"Aves"},
        {"nombre":"Brass Birmingham","precio":310,"stock":3,"categoria":c1,"imagen":"https://picsum.photos/400/300?random=6","descripcion":"Industria"},
        {"nombre":"Código Secreto","precio":60,"stock":15,"categoria":c2,"imagen":"https://picsum.photos/400/300?random=7","descripcion":"Espías"},
        {"nombre":"Dixit","precio":90,"stock":10,"categoria":c2,"imagen":"https://picsum.photos/400/300?random=8","descripcion":"Abstracto"},
        {"nombre":"Party & Co","precio":75,"stock":12,"categoria":c2,"imagen":"https://picsum.photos/400/300?random=9","descripcion":"Fiesta"},
        {"nombre":"Tabú","precio":55,"stock":20,"categoria":c2,"imagen":"https://picsum.photos/400/300?random=10","descripcion":"Palabras"},
        {"nombre":"Just One","precio":55,"stock":12,"categoria":c2,"imagen":"https://picsum.photos/400/300?random=11","descripcion":"Coop fiesta"},
        {"nombre":"Secret Hitler","precio":120,"stock":6,"categoria":c2,"imagen":"https://picsum.photos/400/300?random=12","descripcion":"Política"},
        {"nombre":"UNO","precio":25,"stock":30,"categoria":c3,"imagen":"https://picsum.photos/400/300?random=13","descripcion":"Clásico"},
        {"nombre":"Exploding Kittens","precio":70,"stock":14,"categoria":c3,"imagen":"https://picsum.photos/400/300?random=14","descripcion":"Gatos"},
        {"nombre":"Sushi Go!","precio":45,"stock":18,"categoria":c3,"imagen":"https://picsum.photos/400/300?random=15","descripcion":"Sushi"},
        {"nombre":"Magic","precio":85,"stock":9,"categoria":c3,"imagen":"https://picsum.photos/400/300?random=16","descripcion":"Mazos"},
        {"nombre":"Dominion","precio":150,"stock":7,"categoria":c3,"imagen":"https://picsum.photos/400/300?random=17","descripcion":"Deckbuilding"},
        {"nombre":"Love Letter","precio":30,"stock":20,"categoria":c3,"imagen":"https://picsum.photos/400/300?random=18","descripcion":"Rápido"},
        {"nombre":"Pandemic","precio":160,"stock":7,"categoria":c4,"imagen":"https://picsum.photos/400/300?random=19","descripcion":"Virus"},
        {"nombre":"Spirit Island","precio":250,"stock":4,"categoria":c4,"imagen":"https://picsum.photos/400/300?random=20","descripcion":"Defensa"},
        {"nombre":"Gloomhaven","precio":350,"stock":2,"categoria":c4,"imagen":"https://picsum.photos/400/300?random=21","descripcion":"Épico"},
        {"nombre":"The Crew","precio":65,"stock":11,"categoria":c4,"imagen":"https://picsum.photos/400/300?random=22","descripcion":"Espacio"},
        {"nombre":"Mysterium","precio":160,"stock":5,"categoria":c4,"imagen":"https://picsum.photos/400/300?random=23","descripcion":"Fantasmas"},
        {"nombre":"Robinson Crusoe","precio":280,"stock":3,"categoria":c4,"imagen":"https://picsum.photos/400/300?random=24","descripcion":"Isla"},
        {"nombre":"Ticket to Ride","precio":170,"stock":9,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=25","descripcion":"Trenes"},
        {"nombre":"Carcassonne","precio":120,"stock":13,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=26","descripcion":"Castillos"},
        {"nombre":"Azul","precio":140,"stock":8,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=27","descripcion":"Azulejos"},
        {"nombre":"Splendor","precio":110,"stock":10,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=28","descripcion":"Gemas"},
        {"nombre":"Kingdomino","precio":90,"stock":15,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=29","descripcion":"Reinos"},
        {"nombre":"Catan Junior","precio":110,"stock":10,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=30","descripcion":"Niños"},
        {"nombre":"Labyrinth","precio":85,"stock":8,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=31","descripcion":"Laberinto"},
        {"nombre":"Outfoxed","precio":120,"stock":9,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=32","descripcion":"Zorro"},
        {"nombre":"Patchwork","precio":105,"stock":7,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=33","descripcion":"Costura"},
        {"nombre":"Camel Up","precio":140,"stock":6,"categoria":c5,"imagen":"https://picsum.photos/400/300?random=34","descripcion":"Carreras"},
    ]

    for d in datos:
        Producto.objects.create(**d)
    print("✅ Productos creados")
else:
    print("ℹ️ Ya hay datos")