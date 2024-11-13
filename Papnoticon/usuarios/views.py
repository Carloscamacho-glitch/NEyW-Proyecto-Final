# usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import RegistroUsuarioForm
from .models import Producto, CartItem, Order
from django.contrib import messages
from .scraping import obtener_precios_externos
from django.http import HttpResponse

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            cliente_group = Group.objects.get(name='Cliente')
            user.groups.add(cliente_group)
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

'''
def productos(request):
    # Captura el término de búsqueda del parámetro 'q' en la URL
    query = request.GET.get('q')
    if query:
        # Filtra los productos que contengan el término de búsqueda en su nombre
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        # Muestra todos los productos si no hay búsqueda
        productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})
'''

def productos(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()

    # Obtener los precios externos solo una vez, ya que es solo para "dona"
    precios_externos = obtener_precios_externos("Dona")

    # Debug: imprime los precios externos en la consola
    print(precios_externos)  # Debería mostrar los precios externos en la consola de Django

    # Añadir los precios externos a cada producto
    for producto in productos:
        # Añade los precios de "dona" para cada producto en el contexto
        producto.precios_externos = precios_externos

    return render(request, 'productos.html', {'productos': productos})

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))  # Captura la cantidad seleccionada

    # Verifica si la cantidad es válida
    if cantidad > producto.stock:
        messages.error(request, f"No hay suficiente stock para {producto.nombre}. Stock disponible: {producto.stock}")
        return redirect('productos')

    # Agrega el producto al carrito o actualiza la cantidad si ya existe en el carrito
    cart_item, created = CartItem.objects.get_or_create(user=request.user, producto=producto)
    if created:
        cart_item.cantidad = cantidad
    else:
        cart_item.cantidad += cantidad

    cart_item.save()
    messages.success(request, f"{producto.nombre} agregado al carrito con éxito.")
    return redirect('ver_carrito')

def procesar_pedido(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.producto.precio * item.cantidad for item in cart_items)
    
    # Crear el pedido
    order = Order.objects.create(user=request.user, total=total)
    order.items.set(cart_items)  # Agrega todos los artículos del carrito al pedido
    order.completed = True
    order.save()

    # Reducir el stock de cada producto
    for item in cart_items:
        producto = item.producto
        if producto.stock >= item.cantidad:
            producto.stock -= item.cantidad  # Reduce el stock
            producto.save()
        else:
            # Maneja el caso en el que no hay suficiente stock
            # (por ejemplo, puedes mostrar un mensaje de error)
            return redirect('ver_carrito')  # Redirigir al carrito o mostrar un mensaje de error

    # Limpiar el carrito después de realizar el pedido
    cart_items.delete()

    return redirect('pagina_inicio')

def ver_carrito(request):
    cart_items = CartItem.objects.filter(user=request.user)
    # Calcula el subtotal para cada artículo en el carrito
    cart_items_with_subtotal = [
        {
            'item': item,
            'subtotal': item.producto.precio * item.cantidad
        }
        for item in cart_items
    ]
    # Calcula el total general
    total = sum(item['subtotal'] for item in cart_items_with_subtotal)
    return render(request, 'carrito.html', {'cart_items_with_subtotal': cart_items_with_subtotal, 'total': total})

def actualizar_carrito(request):
    if request.method == 'POST':
        for item_id in request.POST:
            if item_id.startswith('cantidad_'):
                cart_item_id = int(item_id.split('_')[1])
                cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
                nueva_cantidad = int(request.POST[item_id])

                if nueva_cantidad > cart_item.producto.stock:
                    messages.error(request, f"No hay suficiente stock para {cart_item.producto.nombre}. Stock disponible: {cart_item.producto.stock}")
                elif nueva_cantidad < 1:
                    messages.error(request, f"La cantidad mínima para {cart_item.producto.nombre} es 1.")
                else:
                    cart_item.cantidad = nueva_cantidad
                    cart_item.save()
                    messages.success(request, f"Cantidad de {cart_item.producto.nombre} actualizada a {nueva_cantidad}.")
                    
    return redirect('ver_carrito')

def eliminar_del_carrito(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.producto.nombre} ha sido eliminado del carrito.")
    return redirect('ver_carrito')

@login_required
def pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def presentacion(request):
    return render(request, 'presentacion.html')

def contacto(request):
    return render(request, 'contacto.html')

def enviar_mensaje(request):
    if request.method == "POST":
        # Procesa el formulario y envía el mensaje
        return HttpResponse("Mensaje enviado correctamente")
    return redirect('contacto')  # Si se accede a la vista por GET, redirige a la página de contacto

def comentarios(request):
    return render(request, 'comentarios.html')