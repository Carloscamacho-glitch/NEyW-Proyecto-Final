from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Producto, CartItem

@receiver(user_logged_in)
def transferir_carrito(sender, request, user, **kwargs):
    session_cart = request.session.get('cart', [])
    for item in session_cart:
        producto = Producto.objects.get(id=item['producto_id'])
        cart_item, created = CartItem.objects.get_or_create(user=user, producto=producto)
        cart_item.cantidad += item['cantidad']
        cart_item.save()
    request.session['cart'] = []  # Limpia el carrito de la sesión
