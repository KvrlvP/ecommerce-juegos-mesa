from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.IntegerField(default=0) 
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - Stock: {self.stock}"