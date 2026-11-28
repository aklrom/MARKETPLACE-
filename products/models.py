from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.aggregates import Avg
from cloudinary.models import CloudinaryField  # <-- AJOUTER CET IMPORT

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "catégorie"
        verbose_name_plural = "catégories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    class Condition(models.TextChoices):
        NEW = "new", "Neuf"
        LIKE_NEW = "like_new", "Comme neuf"
        GOOD = "good", "Bon état"
        USED = "used", "Occasion"

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    
    # <-- REMPLACER models.ImageField PAR CloudinaryField
    image = CloudinaryField('image', folder='products/', blank=True, null=True)
    
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(
        max_length=20,
        choices=Condition.choices,
        default=Condition.GOOD,
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Article actif / en vente",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_active", "-created_at"])]

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.is_active and self.quantity > 0

    @property
    def average_rating(self):
        result = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(result, 1) if result is not None else 0.0

    @property
    def reviews_count(self):
        return self.reviews.count()