from urllib.parse import quote

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.db.models import F
from django.utils import timezone

from products.models import Product


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "En attente"
        CANCELLED = "cancelled", "Annulée"
        COMPLETED = "completed", "Terminée"

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    # Prix figé au moment de la commande : copié depuis le produit côté serveur.
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    seller_confirmed = models.BooleanField("confirmée par le vendeur", default=False)
    buyer_confirmed = models.BooleanField("confirmée par l'acheteur", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "commande"
        verbose_name_plural = "commandes"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"])]

    def __str__(self):
        return f"Commande #{self.pk} - {self.product.name}"

    
    @property
    def total(self):
        return self.unit_price * self.quantity

    @property
    def seller(self):
        return self.product.seller

    @property
    def can_cancel(self):
        return self.status == self.Status.PENDING and not (
            self.seller_confirmed or self.buyer_confirmed
        )

    @staticmethod
    def _whatsapp_link(user, text):
        number = (user.whatsapp_number or "").lstrip("+")
        return f"https://wa.me/{number}?text={quote(text)}"

    @property
    def contact_seller_link(self):
        """Lien WhatsApp vers le vendeur (à afficher à l'acheteur uniquement)."""
        text = (
            f"Bonjour, je vous contacte au sujet de ma commande #{self.pk} "
            f"({self.quantity} × {self.product.name})."
        )
        return self._whatsapp_link(self.product.seller, text)

    @property
    def contact_buyer_link(self):
        """Lien WhatsApp vers l'acheteur (à afficher au vendeur uniquement)."""
        text = (
            f"Bonjour, je vous contacte au sujet de la commande #{self.pk} "
            f"({self.quantity} × {self.product.name})."
        )
        return self._whatsapp_link(self.buyer, text)

    
    @classmethod
    def _locked(cls, order_id):
        return (
            cls.objects.select_for_update(of=("self",))
            .select_related("product")
            .get(pk=order_id)
        )

    @classmethod
    def cancel_by(cls, order_id, user):
        """Annule une commande en attente et remet le stock. Acheteur ou vendeur."""
        with transaction.atomic():
            order = cls._locked(order_id)

            if user.pk not in (order.buyer_id, order.product.seller_id):
                raise PermissionDenied("Vous n'avez pas le droit de gérer cette commande.")
            if order.status != cls.Status.PENDING:
                raise PermissionDenied("Cette commande ne peut plus être annulée.")
            if order.seller_confirmed or order.buyer_confirmed:
                raise PermissionDenied(
                    "Cette commande a déjà été validée par l'une des parties. "
                    "Impossible de l'annuler."
                )

            order.status = cls.Status.CANCELLED
            order.save(update_fields=["status", "updated_at"])
            Product.objects.filter(pk=order.product_id).update(
                quantity=F("quantity") + order.quantity,
                updated_at=timezone.now(),
            )
        return order

    @classmethod
    def confirm_as_seller(cls, order_id, user):
        return cls._confirm(order_id, user, role="seller")

    @classmethod
    def confirm_as_buyer(cls, order_id, user):
        return cls._confirm(order_id, user, role="buyer")

    @classmethod
    def _confirm(cls, order_id, user, role):
        with transaction.atomic():
            order = cls._locked(order_id)

            if role == "seller":
                expected_user_id = order.product.seller_id
                field = "seller_confirmed"
            else:
                expected_user_id = order.buyer_id
                field = "buyer_confirmed"

            if user.pk != expected_user_id:
                raise PermissionDenied("Vous n'êtes pas autorisé à valider cette commande.")
            if order.status != cls.Status.PENDING:
                raise PermissionDenied("Cette commande ne peut plus être validée.")
            if getattr(order, field):
                raise PermissionDenied("Vous avez déjà validé cette commande.")

            setattr(order, field, True)
            update_fields = [field, "updated_at"]

            if order.seller_confirmed and order.buyer_confirmed:
                order.status = cls.Status.COMPLETED
                order.completed_at = timezone.now()
                update_fields += ["status", "completed_at"]

            order.save(update_fields=update_fields)
        return order