from django import forms
from django.contrib.auth.models import User
from .models import Productos, Proveedor, SalidaProducto, UserProfile


class ProductoForm(forms.ModelForm):
    class Meta:
        model= Productos
        fields = ['nombre', 'codigo', 'descripcion', 'precio', 'stock', 'categoria', 'proveedor']

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
    
class ImportarExcelForm(forms.Form):
    archivo_excel = forms.FileField(
        label='Archivo Excel',
        help_text='Seleccione el archivo Excel con los productos a importar',
        widget=forms.FileInput(attrs={'accept': '.xlsx,.xls'})
    )


class RegistroUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=150)
    last_name = forms.CharField(label='Apellido', max_length=150)
    email = forms.EmailField(label='Correo')
    telefono = forms.CharField(label='Teléfono (opcional)', max_length=20, required=False)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Usuario',
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El nombre de usuario ya existe')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El correo ya está registrado')
        return email

    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        password_confirm = cleaned.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                telefono=self.cleaned_data.get('telefono', '')
            )
        return user

