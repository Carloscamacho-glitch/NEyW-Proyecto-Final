from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Importa auth_views para manejar las vistas de autenticación
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.pagina_inicio, name='pagina_inicio'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Página de login
    path('logout/', views.cerrar_sesion, name='logout'),  # Ruta para cerrar sesión
    path('productos/', views.productos, name='productos'), # PRODUCTOS
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver_carrito/', views.ver_carrito, name='ver_carrito'),
    path('actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),  # Ruta para actualizar cantidades
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),  # Ruta para eliminar del carrito
    path('contacto/', views.contacto, name='contacto'), # Ruta para contactarnos
    path('comentarios/', views.obtener_tweets, name='comentarios'), # Ruta para los comentarios de twitter
    path('checkout/', views.checkout, name='checkout'), # Ruta para hacer checkout
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'), # Ruta de pago exitoso
    path('mis_planes/', views.mis_planes, name='mis_planes'), # Ruta de planes comprados
    path('descargar_txt/<int:pedido_id>/', views.descargar_archivo_txt, name='descargar_archivo_txt'), #Ruta para descargar detalles del pedido
    path('descargar_exe/<int:pedido_id>/', views.descargar_archivo_exe, name='descargar_archivo_exe'), #Ruta para descargar el programa
    path('facebook/', views.mostrar_publicacion, name='mostrar_publicacion'),
    path('publicar/', views.publicar, name='publicar'),
    path('programar/', views.programar, name='programar'),
    path('subir_imagen/', views.subir_imagen, name='subir_imagen'),
    path('eliminar/', views.eliminar, name='eliminar'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
