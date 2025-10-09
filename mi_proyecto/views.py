from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Productos, Proveedor, SalidaProducto, HistorialMovimiento
from django.forms import formset_factory
from django.contrib import messages
from .forms import ProductoForm, MultipleProductosForm, ProveedorForm

def inicio(request):
    # Estadísticas de productos
    total_productos = len(Productos.objects.all())
    total_proveedores = len(Proveedor.objects.all())
    productos_bajo_stock = len(Productos.objects.filter(stock__lt=5))
    
    # Productos recientes
    productos_recientes = Productos.objects.order_by('-fecha_ingreso')[:5]
    
    context = {
        'total_productos': total_productos,
        'total_proveedores': total_proveedores,
        'productos_bajo_stock': productos_bajo_stock,
        'productos_recientes': productos_recientes,
    }
    return render(request, 'mi_proyecto/inicio.html', context)

def lista_productos(request):
    categoria_seleccionada = request.GET.get('categoria', 'todos')
    busqueda = request.GET.get('busqueda', '')
    page = request.GET.get('page', 1)
    items_per_page = 10
    
    # Base query con ordenamiento #######################
    productos = Productos.objects.all().order_by('nombre')
    
    # Filtro por categoría #############################
    if categoria_seleccionada != 'todos':
        productos = productos.filter(categoria=categoria_seleccionada)
    
    # Búsqueda por nombre o código ###################
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)
    
    # Paginador #############################
    paginator = Paginator(productos, items_per_page)
    
    try:
        productos_paginados = paginator.page(page)
    except PageNotAnInteger:
        productos_paginados = paginator.page(1)
    except EmptyPage:
        productos_paginados = paginator.page(paginator.num_pages)
    
    context = {
        'productos': productos_paginados,
        'categorias': Productos.CATEGORIAS,
        'categoria_actual': categoria_seleccionada,
        'busqueda': busqueda,
    }
    return render(request, 'mi_proyecto/lista_productos.html', context)

def crear_producto(request):
    form = ProductoForm()
    form_multiple = MultipleProductosForm()
    modo_multiple = False
    formset = None

    if request.method == 'POST':
        if 'crear_multiple' in request.POST:
            form_multiple = MultipleProductosForm(request.POST)
            if form_multiple.is_valid():
                cantidad = form_multiple.cleaned_data['cantidad']
                ProductoFormSet = formset_factory(ProductoForm, extra=cantidad)
                formset = ProductoFormSet()
                modo_multiple = True

        elif 'guardar_multiple' in request.POST:
            ProductoFormSet = formset_factory(ProductoForm)
            formset = ProductoFormSet(request.POST)
            if formset.is_valid():
                creados = 0
                for f in formset:
                    if f.has_changed():
                        producto = f.save()
                        # Registrar en historial
                        HistorialMovimiento.objects.create(
                            producto=producto,
                            nombre_producto=producto.nombre,
                            serial_producto=producto.codigo,
                            usuario=request.user if request.user.is_authenticated else None,
                            tipo_movimiento='CREACION',
                            detalles='Creación múltiple de productos'
                        )
                        creados += 1
                messages.success(request, f'Se crearon {creados} producto(s).')
                return redirect('lista_productos')
            modo_multiple = True

        else:
            form = ProductoForm(request.POST)
            if form.is_valid():
                producto = form.save()
                # Registrar en historial
                HistorialMovimiento.objects.create(
                    producto=producto,
                    nombre_producto=producto.nombre,
                    serial_producto=producto.codigo,
                    usuario=request.user if request.user.is_authenticated else None,
                    tipo_movimiento='CREACION',
                    detalles='Creación de producto'
                )
                messages.success(request, 'Producto creado exitosamente.')
                return redirect('lista_productos')

    return render(request, 'mi_proyecto/crear_producto.html', {
        'form': form,
        'form_multiple': form_multiple,
        'modo_multiple': modo_multiple,
        'formset': formset
    })

def editar_producto(request, id):
    producto = get_object_or_404(Productos, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            # Registrar en historial
            HistorialMovimiento.objects.create(
                producto=producto,
                nombre_producto=producto.nombre,
                serial_producto=producto.codigo,
                usuario=request.user if request.user.is_authenticated else None,
                tipo_movimiento='EDICION',
                detalles='Edición de producto'
            )
            messages.success(request, f'Producto "{producto.nombre}" actualizado exitosamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'mi_proyecto/editar_producto.html', {'form': form, 'producto': producto})

def eliminar_producto(request, id):
    producto = get_object_or_404(Productos, id=id)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'mi_proyecto/eliminar_producto.html', {'producto': producto})  


# Proveedor #####################################################

def lista_proveedores(request):
    page = request.GET.get('page', 1)
    items_per_page = 10

    proveedores_qs = Proveedor.objects.all().order_by('nombre')
    paginator = Paginator(proveedores_qs, items_per_page)
    try:
        proveedores = paginator.page(page)
    except PageNotAnInteger:
        proveedores = paginator.page(1)
    except EmptyPage:
        proveedores = paginator.page(paginator.num_pages)

    return render(request, 'mi_proyecto/proveedor/lista_proveedores.html', {
        'proveedores': proveedores
    })

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'mi_proyecto/proveedor/crear_proveedor.html', {'form': form})


def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('lista_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'mi_proyecto/proveedor/editar_proveedor.html', {
        'form': form,
        'proveedor': proveedor
    })

def eliminar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('lista_proveedores')
    return render(request, 'mi_proyecto/proveedor/eliminar_proveedor.html', {'proveedor': proveedor})


#Historial de movimientos #####################################################

def historial_movimientos(request):
    categoria_seleccionada = request.GET.get('categoria', 'todos')
    page = request.GET.get('page', 1)
    items_per_page = 10

    movimientos_qs = HistorialMovimiento.objects.select_related('producto', 'usuario').order_by('-fecha_movimiento')
    if categoria_seleccionada != 'todos':
        movimientos_qs = movimientos_qs.filter(producto__categoria=categoria_seleccionada)

    paginator = Paginator(movimientos_qs, items_per_page)
    try:
        movimientos = paginator.page(page)
    except PageNotAnInteger:
        movimientos = paginator.page(1)
    except EmptyPage:
        movimientos = paginator.page(paginator.num_pages)

    return render(request, 'mi_proyecto/historial_movimientos.html', {
        'movimientos': movimientos,
        'categoria_actual': categoria_seleccionada,
        'categorias': Productos.CATEGORIAS,
    })


