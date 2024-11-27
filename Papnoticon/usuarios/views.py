# usuarios/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required
from .scraping2 import obtener_precios_externos2
from .scraping import obtener_precios_externos
from .models import Producto, CartItem, Order
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from .forms import RegistroUsuarioForm
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .forms import ContactForm
import tweepy, stripe, csv

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

def productos(request):
    query = request.GET.get('q')
    if query:
        productos = Producto.objects.filter(nombre__icontains=query)
    else:
        productos = Producto.objects.all()

    # Mapear cada producto con el plan que se requiere buscar
    plan_map = {
        "Familiar": "Familiar",
        "Individual": "Individual",
        "Estudiantes": "Estudiantes"
    }

    for producto in productos:
        # Determina el nombre del plan a buscar según el nombre del producto
        plan_nombre = plan_map.get(producto.nombre, None)
        if plan_nombre:
            # Obtener precios de la primera fuente
            precios_externos = obtener_precios_externos(plan_nombre)
            # Obtener precios de la segunda fuente
            precios_otro = obtener_precios_externos2(plan_nombre)

            #Añadir ambos resultados al producto
            producto.precios_externos = precios_externos
            producto.precios_otro = precios_otro

    return render(request, 'productos.html', {'productos': productos})

def pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def presentacion(request):
    return render(request, 'presentacion.html')

def contacto(request):
    mensaje_enviado = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Aquí puedes manejar el envío del mensaje, por ejemplo, enviarlo por correo electrónico.
            mensaje_enviado = True
            # Puedes realizar cualquier otra acción, como guardar el mensaje en la base de datos.

    else:
        form = ContactForm()

    return render(request, 'contacto.html', {
        'form': form,
        'mensaje_enviado': mensaje_enviado
    })

def enviar_mensaje(request):
    if request.method == "POST":
        # Procesa el formulario y envía el mensaje
        return HttpResponse("Mensaje enviado correctamente")
    return redirect('contacto')  # Si se accede a la vista por GET, redirige a la página de contacto

def comentarios(request):
    return render(request, 'comentarios.html')

# Vista para obtener comentarios de Twitter
def obtener_tweets(request):
    bearer_token = settings.TWITTER_BEARER_TOKEN

    client = tweepy.Client(bearer_token=bearer_token)
    tweets = []

    try:
        query = "#Hola"
        # Solicitar tweets con información de los autores y medios
        response = client.search_recent_tweets(
            query=query,
            max_results=10,
            tweet_fields=['text', 'author_id'],
            expansions='author_id,attachments.media_keys',
            user_fields=['username'],
            media_fields=['url']  # Obtener la URL de los medios (imágenes)
        )

        if response.data:
            # Crear un diccionario para obtener los nombres de usuario
            user_map = {user.id: user.username for user in response.includes['users']}
            media_map = {media.media_key: media.url for media in response.includes['media']}  # Mapeo de media_key a url

            for tweet in response.data:
                author_username = user_map.get(tweet.author_id, "Usuario desconocido")
                media_urls = []  # Lista de URLs de medios
                if 'attachments' in tweet.data:
                    # Si hay medios adjuntos, obtener las URLs correspondientes
                    for media_key in tweet.data['attachments']['media_keys']:
                        media_url = media_map.get(media_key)
                        if media_url:
                            media_urls.append(media_url)

                # Agregar el tweet y las imágenes (si existen)
                tweets.append({
                    'texto': tweet.text,
                    'autor': author_username,
                    'media_urls': media_urls  # Lista de URLs de imágenes
                })
        else:
            print("No se encontraron tweets.")

    except tweepy.TweepyException as e:
        print(f"Error al conectar con la API de Twitter: {e}")

    return render(request, 'comentarios.html', {'tweets': tweets})

def cerrar_sesion(request):
    """Cierra la sesión del usuario y redirige a la página de inicio."""
    logout(request)  # Cierra la sesión del usuario actual
    return redirect('/')  # Redirige a la página de inicio


#carrito
@login_required
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

@login_required
def ver_carrito(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_items_with_subtotal = [
        {
            'item': item,
            'subtotal': item.producto.precio * item.cantidad
        }
        for item in cart_items
    ]
    total = sum(item['subtotal'] for item in cart_items_with_subtotal)
    return render(
        request,
        'carrito.html',
        {
            'cart_items_with_subtotal': cart_items_with_subtotal,
            'total': total,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,  # Aquí se pasa la clave
        }
    )

@login_required
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

@login_required
def eliminar_del_carrito(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    messages.success(request, f"{cart_item.producto.nombre} ha sido eliminado del carrito.")
    return redirect('ver_carrito')


#Pasarela de pagos
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    line_items = []

    for item in cart_items:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.producto.nombre,
                },
                'unit_amount': int(item.producto.precio * 100),  # Stripe trabaja en centavos
            },
            'quantity': item.cantidad,
        })

    # Configura la sesión de Stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('pago_exitoso')) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('ver_carrito')),
    )

    return JsonResponse({'id': session.id})

@login_required
def pago_exitoso(request):
    session_id = request.GET.get('session_id')  # Identificador del pago

    # Obtener los items del carrito
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.producto.precio * item.cantidad for item in cart_items)

    if not cart_items.exists():
        messages.error(request, "No hay productos en el carrito.")
        return redirect('ver_carrito')

    if session_id:  # Verificar si el pago fue exitoso
        # Crear el pedido
        order = Order.objects.create(user=request.user, total=total)
        order.items.set(cart_items)  # Asignar los artículos del carrito al pedido
        order.completed = True
        order.save()

        # Reducir el stock de cada producto
        for item in cart_items:
            producto = item.producto
            if producto.stock >= item.cantidad:
                producto.stock -= item.cantidad  # Descontar del stock
                producto.save()
            else:
                # Manejar caso de stock insuficiente (aunque no debería ocurrir después del pago)
                messages.error(request, f"No hay suficiente stock para {producto.nombre}.")
                return redirect('ver_carrito')

        # Limpiar el carrito después del pedido
        cart_items.delete()

        messages.success(request, "¡Pedido procesado y pago realizado con éxito!")
        return redirect('ver_carrito')
    else:
        # Si no hay un `session_id`, asume que el pago no se realizó
        messages.error(request, "No se pudo completar el pago. Inténtalo de nuevo.")
        return redirect('ver_carrito')

@login_required
def mis_planes(request):
    # Obtener los pedidos completados del usuario
    pedidos = Order.objects.filter(user=request.user, completed=True)

    # Verificar si hay pedidos
    if not pedidos.exists():
        return render(request, 'mis_planes.html', {'pedidos': None})

    return render(request, 'mis_planes.html', {'pedidos': pedidos})

#Descargar archivos
@login_required
def descargar_archivo_txt(request, pedido_id):
    pedido = get_object_or_404(Order, id=pedido_id, user=request.user)

    # Crear el contenido del archivo de texto
    contenido = f"Detalles del Pedido #{pedido.id}\n"
    contenido += f"Fecha: {pedido.created_at.strftime('%d-%m-%Y')}\n"
    contenido += f"Total: ${pedido.total}\n\n"
    contenido += "-" * 40 + "\n"
    contenido += "-" * 40 + "\n"
    contenido += "\n"
    contenido += "Gracias por tu compra.\n"

    # Crear la respuesta HTTP para descargar el archivo
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="pedido_{pedido.id}.txt"'
    response.write(contenido)
    return response

@login_required
def descargar_archivo_exe(request, pedido_id):
    pedido = get_object_or_404(Order, id=pedido_id, user=request.user)

    # Ruta del archivo .exe en el servidor
    ruta_exe = 'static\EXE\Hola.exe'

    # Crear la respuesta para el archivo .exe
    response_exe = FileResponse(open(ruta_exe, 'rb'), content_type='application/octet-stream')
    response_exe['Content-Disposition'] = 'attachment; filename="instalador.exe"'

    # Regresar ambas descargas como opciones al usuario (uno tras otro).
    return response_exe