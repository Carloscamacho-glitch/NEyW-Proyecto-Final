from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=10)  # Nuevo campo para el inventario

    def __str__(self):
        return self.nombre

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'created_at', 'completed')  # Campos visibles en la lista
    list_filter = ('completed', 'created_at')  # Filtros laterales
    search_fields = ('user__username', 'id')  # Campo de búsqueda
    actions = ['delete_selected_orders']  # Agregar una acción personalizada

    def delete_selected_orders(self, request, queryset):
        """
        Eliminar pedidos seleccionados junto con sus items relacionados.
        """
        for order in queryset:
            order.items.all().delete()  # Eliminar los elementos relacionados
            order.delete()  # Eliminar el pedido
        self.message_user(request, f"Se eliminaron {queryset.count()} pedidos correctamente.")

    delete_selected_orders.short_description = "Eliminar pedidos seleccionados"
