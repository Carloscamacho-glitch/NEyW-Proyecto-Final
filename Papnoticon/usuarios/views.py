# usuarios/views.py
from .selenium_scraper import compare_prices
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, CartItem, Order
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from .forms import RegistroUsuarioForm
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .forms import ContactForm
from datetime import datetime
import tweepy, stripe, csv, requests
import os, json

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

    # Llamamos a la función que obtiene los precios y planes de los servicios externos
    precios_y_planes = compare_prices()

    # Pasar tanto los productos como los precios y planes al renderizado
    return render(request, 'productos.html', {
        'productos': productos,
        'precios_y_planes': precios_y_planes
    })
def pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def presentacion(request):
    return render(request, 'presentacion.html')

def publicaciones(request):
    return render(request, 'facebook.html')

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

# Función para obtener el PAGE_ACCESS_TOKEN automáticamente
def obtener_page_access_token(user_access_token, page_id):
    url = f"https://graph.facebook.com/v21.0/me/accounts?access_token={user_access_token}"
    response = requests.get(url)
def pagina_inicio(request):
    return render(request, 'pagina_inicio.html')

def presentacion(request):
    return render(request, 'presentacion.html')

def publicaciones(request):
    return render(request, 'facebook.html')

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

# Función para obtener el PAGE_ACCESS_TOKEN automáticamente
def obtener_page_access_token(user_access_token, page_id):
    url = f"https://graph.facebook.com/v21.0/me/accounts?access_token={user_access_token}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for page in data.get("data", []):
            if page["id"] == page_id:
                return page["access_token"]
        print(f"Página con ID {page_id} no encontrada.")
        return None
    else:
        raise Exception(f"Error al obtener el token de la página: {response.text}")

# Función auxiliar para registrar publicaciones en un archivo
def registrar_publicacion(post_id, mensaje, tipo):
    archivo = "publicaciones_log.txt"
    ruta_absoluta = os.path.abspath(archivo)
    print(f"El archivo se intentará crear en: {ruta_absoluta}")  # Debug
    try:
        with open(archivo, "a") as file:
            hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"[{hora_actual}] {tipo} | Post ID: {post_id} | Mensaje: {mensaje}\n")
        print(f"Publicación registrada en el archivo '{ruta_absoluta}'.")
    except Exception as e:
        print(f"Error al escribir en el archivo '{ruta_absoluta}': {e}")


# Funciones auxiliares de publicación
def publicar_en_pagina(page_id, mensaje, page_access_token):
    url = f"https://graph.facebook.com/v21.0/{page_id}/feed"
    params = {"message": mensaje, "access_token": page_access_token}
    response = requests.post(url, params=params)
    return response.json()


def programar_publicacion(page_id, mensaje, tiempo_programado, page_access_token):
    url = f"https://graph.facebook.com/v21.0/{page_id}/feed"
    params = {
        "message": mensaje,
        "published": False,
        "scheduled_publish_time": tiempo_programado,
        "access_token": page_access_token
    }
    response = requests.post(url, params=params)
    return response.json()


def subir_imagen(page_id, imagen_path, mensaje, page_access_token):
    try:
        if not isinstance(page_access_token, str) or not page_access_token.strip():
            return {"status": "error", "message": "El token de acceso no es válido o está vacío."}

        url = f"https://graph.facebook.com/v21.0/{page_id}/photos"
        with open(imagen_path, "rb") as img_file:
            files = {"source": img_file}
            params = {"message": mensaje, "access_token": page_access_token}

            print(f"URL: {url}")
            print(f"Params: {params}")
            
            response = requests.post(url, files=files, data=params)

        if response.status_code == 200:
            resultado = response.json()
            if "post_id" in resultado:
                return {"status": "success", "post_id": resultado["post_id"]}
            else:
                return {"status": "error", "message": "Imagen subida, pero no se devolvió el ID de la publicación."}
        else:
            try:
                error_data = response.json()
            except ValueError:
                error_data = {"error": "No se pudo parsear la respuesta del servidor"}

            return {
                "status": "error",
                "message": error_data.get("error", "Error desconocido"),
                "details": response.text
            }
    except Exception as e:
        return {"status": "error", "message": str(e)}



def eliminar_publicacion(post_id, page_access_token):
    url = f"https://graph.facebook.com/v21.0/{post_id}"
    params = {"access_token": page_access_token}
    response = requests.delete(url, params=params)
    return response.json()


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

@login_required
def mostrar_publicacion(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'facebook.html')  # Renderiza la plantilla directamente
    return redirect('login')  # Redirige al login si no está autenticado


@login_required  # Asegura que solo usuarios autenticados puedan acceder
@csrf_exempt
def publicar(request):
    if not request.user.is_staff:  # Verifica si el usuario es administrador
        return JsonResponse({"status": "error", "message": "Permiso denegado."}, status=403)
    
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        mensaje = data.get('mensaje', '')
        
        # Obtener el PAGE_ACCESS_TOKEN
        PAGE_ACCESS_TOKEN = obtener_page_access_token(settings.FACEBOOK_USER_ACCESS_TOKEN, '481272215072996')
        
        # Realizar la publicación
        resultado = publicar_en_pagina('481272215072996', mensaje, PAGE_ACCESS_TOKEN)

        if 'id' in resultado:
            registrar_publicacion(resultado['id'], mensaje, 'Publicación de texto')

        return JsonResponse(resultado)
    return JsonResponse({"status": "error", "message": "Método no permitido."}, status=405)
    

@login_required  # Asegura que solo usuarios autenticados puedan acceder
@csrf_exempt  # Desactiva protección CSRF, necesaria para usar request.body directamente
def programar(request):
    if not request.user.is_staff:  # Verifica si el usuario es administrador
        return JsonResponse({"status": "error", "message": "Permiso denegado."}, status=403)

    if request.method == 'POST':
        import json
        data = json.loads(request.body)  # Procesa el JSON recibido
        mensaje = data.get('mensaje', '')
        tiempo_programado = int(data.get('tiempo_programado', 0))

        # Obtener el PAGE_ACCESS_TOKEN
        PAGE_ACCESS_TOKEN = obtener_page_access_token(settings.FACEBOOK_USER_ACCESS_TOKEN, '481272215072996')

        # Realizar la programación de la publicación
        resultado = programar_publicacion('481272215072996', mensaje, tiempo_programado, PAGE_ACCESS_TOKEN)

        if 'id' in resultado:
            registrar_publicacion(resultado['id'], mensaje, 'Publicación Programada')

        return JsonResponse(resultado)

@login_required  # Asegura que solo usuarios autenticados puedan acceder
@csrf_exempt  # Necesario para manejar datos de formularios sin CSRF
def subir_imagen(request):
    if not hasattr(request, 'user') or not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Usuario no autenticado."}, status=401)

    if not request.user.is_staff:  # Verifica si el usuario es administrador
        return JsonResponse({"status": "error", "message": "Permiso denegado."}, status=403)

    if request.method == 'POST':
        import json
        try:
            mensaje = request.POST.get('mensaje', '')
            imagen = request.FILES.get('imagen')

            if not imagen:
                return JsonResponse({"status": "error", "message": "No se proporcionó ninguna imagen."})

            # Guardar la imagen temporalmente
            temp_dir = "./temp"
            os.makedirs(temp_dir, exist_ok=True)
            imagen_path = os.path.join(temp_dir, imagen.name)

            with open(imagen_path, 'wb+') as destination:
                for chunk in imagen.chunks():
                    destination.write(chunk)

            # Obtener el PAGE_ACCESS_TOKEN
            PAGE_ACCESS_TOKEN = obtener_page_access_token(settings.FACEBOOK_USER_ACCESS_TOKEN, '481272215072996')
            if not PAGE_ACCESS_TOKEN:
                return JsonResponse({"status": "error", "message": "No se pudo obtener el token de acceso."})

            # Subir la imagen a Facebook
            resultado = subir_imagen('481272215072996', imagen_path, mensaje, PAGE_ACCESS_TOKEN)

            if not isinstance(resultado, dict):
                return JsonResponse({"status": "error", "message": "Respuesta inesperada de subir_imagen."})

            if resultado.get("status") == "success":
                registrar_publicacion(resultado["post_id"], mensaje, "Publicación de imagen")

            # Eliminar el archivo temporal
            os.remove(imagen_path)
            return JsonResponse(resultado)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
@login_required  # Asegura que solo usuarios autenticados puedan acceder
@csrf_exempt  # Necesario para usar request.body directamente
def eliminar(request):
    if not request.user.is_staff:  # Verifica si el usuario es administrador
        raise PermissionDenied("No tienes permiso para realizar esta acción.")

    if request.method == 'DELETE':
        data = json.loads(request.body)  # Procesa el JSON recibido
        post_id = data.get('post_id')

        if not post_id:
            return JsonResponse({"status": "error", "message": "Falta el ID de la publicación."})

        # Obtener el PAGE_ACCESS_TOKEN
        PAGE_ACCESS_TOKEN = obtener_page_access_token(settings.FACEBOOK_USER_ACCESS_TOKEN, '481272215072996')

        # Eliminar la publicación en Facebook
        resultado = eliminar_publicacion(post_id, PAGE_ACCESS_TOKEN)

        return JsonResponse(resultado)