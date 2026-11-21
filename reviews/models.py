from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from products.models import Product


class Review(models.Model):
    publier = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="review",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    text = models.TextField()
    rating = models.IntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")],
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'publier')  # 1a: Un seul avis par produit et par utilisateur
        ordering = ['-created_at']

    def __str__(self):
        return f"Avis de {self.publier} sur {self.product}"

    def clean(self):
        super().clean()
        if not self.text or not self.text.strip():
            raise ValidationError({"text": "Le commentaire ne peut pas être vide."})
