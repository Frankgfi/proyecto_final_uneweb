from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Productos(models.Model):
    CATEGORIAS = [
        ('COMPUTADORAS', 'Computadoras'),
        ('LAPTOPS', 'Laptops'),
        ('UPS', 'UPS'),
        ('PERIFERICOS', 'Periféricos'),
    ]

    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=500)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    fecha_ingreso = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey('Proveedor',on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Proveedor")
    
    def __str__(self):
        return self.nombre


class HistorialMovimiento(models.Model):
    TIPO_MOVIMIENTO = [
        ('CREACION', 'creacion'),
        ('EDICION', 'edicion'),
        ('ELIMINACION', 'eliminacion'),
    ]    

    producto = models.ForeignKey(Productos, on_delete=models.SET_NULL, null=True, related_name='historial')
    nombre_producto = models.CharField(max_length=100, blank=True)
    serial_producto = models.CharField(max_length=50, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_MOVIMIENTO)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField(blank=True)

class SalidaProducto(models.Model):
    MOTIVOS = [
        ('VENTA', 'Venta'),
        ('GARANTIA', 'Garantía'),
        ('DEVOLUCION', 'Devolución al proveedor'),
        ('DONACION', 'Donación'),
        ('OTRO', 'Otro'),
    ]
    
    producto = models.ForeignKey(Productos, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    motivo = models.CharField(max_length=20, choices=MOTIVOS)
    descripcion = models.TextField(blank=True, help_text="Detalles adicionales sobre la salida")
    fecha_salida = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)  
    contacto = models.CharField(max_length=100, blank=True)  # Persona de contacto (opcional)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.nombre