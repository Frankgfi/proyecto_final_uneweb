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

from django import forms

class MultipleProductosForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, max_value=50, initial=1, label='Cantidad de formularios')


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'direccion', 'telefono', 'email']
        labels = {
            'contacto': 'Persona de contacto',
        }
        
class SalidaProductoForm(forms.ModelForm):
    class Meta:
        model = SalidaProducto
        fields = ['producto', 'cantidad', 'motivo', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtramos solo los productos que tienen stock
        self.fields['producto'].queryset = Productos.objects.filter(stock__gt=0)
    
    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        producto = self.cleaned_data.get('producto')
        
        if producto and cantidad > producto.stock:
            raise forms.ValidationError(f"No hay suficiente stock. Stock disponible: {producto.stock}")
        
        return cantidad