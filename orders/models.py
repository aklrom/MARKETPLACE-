from django.db import models
from django.conf import settings

from products.models import Product 

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("cancelled", "Annulée"),
        ("completed", "Terminée")
    ]
    buyer=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    product =models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="orders"
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    seller_status=models.BooleanField(default=False)
    buyer_status=models.BooleanField(default=False)

    def __str__(self):
        return f"Commande #{self.id} - {self.product.name}"
# Create your models here.
