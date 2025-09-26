from django import forms
from .models import Productos, Proveedor, SalidaProducto

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'direccion', 'telefono', 'email']

class ProductoForm(forms.ModelForm):
    class Meta:
        model= Productos
        fields = ['nombre', 'codigo', 'descripcion', 'precio', 'stock', 'categoria', 'proveedor']

class SalidaProductoForm(forms.ModelForm):
    class Meta:
        model= SalidaProducto
        fields = ['producto', 'cantidad', 'motivo', 'descripcion']

def clean_cantidad(self):
    cantidad = self.cleaned_data['cantidad']
    producto = self.cleaned_data.get('producto')
    if producto and cantidad > producto.stock:
        raise forms.ValidationError(f"No hay suficiente stock. Stock disponible: {producto.stock}")
    return cantidad
