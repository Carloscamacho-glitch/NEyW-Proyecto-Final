from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Importa auth_views para manejar las vistas de autenticación
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.presentacion, name='presentacion'),
    path('registro/', views.registro, name='registro'),
    path('inicio/', views.pagina_inicio, name='pagina_inicio'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Página de login
    path('logout/', auth_views.LogoutView.as_view(next_page='presentacion'), name='logout'),  # Ruta para cerrar sesión
    path('productos/', views.productos, name='productos'), # PRODUCTOS
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('procesar_pedido/', views.procesar_pedido, name='procesar_pedido'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),  # Ruta para actualizar cantidades
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),  # Ruta para eliminar del carrito
    path('contacto/', views.contacto, name='contacto'),
    path('enviar_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('comentarios/', views.comentarios, name='comentarios'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
