from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Productos, Proveedor, SalidaProducto

def inicio(request):
    # Estadísticas básicas
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
    
    # Base query con ordenamiento
    productos = Productos.objects.all().order_by('nombre')
    
    # Filtro por categoría
    if categoria_seleccionada != 'todos':
        productos = productos.filter(categoria=categoria_seleccionada)
    
    # Búsqueda por nombre o código
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)
    
    # Crear el paginador
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