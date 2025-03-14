from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

CATEGORY = (
    ('Stationary', 'Stationary'),
    ('Electronics', 'Electronics'),
    ('Food', 'Food'),
)

class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    stock = models.PositiveIntegerField(null=True)  # Se cambia 'quantity' a 'stock'
    category = models.CharField(max_length=50, choices=CATEGORY, null=True)

    def __str__(self):
        return f'{self.name} - Stock: {self.stock}'

class Order(models.Model):
    name = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)

    def clean(self):
        """Validación para evitar pedidos superiores al stock."""
        if self.order_quantity and self.name and self.order_quantity > self.name.stock:
            raise ValidationError(f'Solo hay {self.name.stock} unidades disponibles de {self.name}.')

    def save(self, *args, **kwargs):
        """Verifica stock antes de guardar y lo descuenta si es válido."""
        self.clean()  # Llamar a la validación
        self.name.stock -= self.order_quantity  # Restar del inventario
        self.name.save()  # Guardar cambios en el producto
        super().save(*args, **kwargs)  # Guardar la orden

    def __str__(self):
        return f'{self.customer} - {self.name} ({self.order_quantity})'