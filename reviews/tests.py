from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError

from accounts.models import User
from orders.models import Order
from products.models import Category, Product
from .models import Review


class ReviewTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(
            whatsapp_number="+22997000001",
            password="test-pass",
            first_name="Acheteur",
            last_name="Test",
        )
        self.other = User.objects.create_user(
            whatsapp_number="+22997000002",
            password="test-pass",
            first_name="Autre",
            last_name="Test",
        )
        self.seller = User.objects.create_user(
            whatsapp_number="+22997000003",
            password="test-pass",
            first_name="Vendeur",
            last_name="Test",
        )
        self.category = Category.objects.create(name="Sport")
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name="Ballon",
            description="Un ballon",
            price="1000",
            quantity=5,
        )
        self.completed_order = Order.objects.create(
            buyer=self.buyer,
            product=self.product,
            quantity=1,
            unit_price="1000",
            status=Order.Status.COMPLETED,
        )

    def test_login_required_to_create_review(self):
        response = self.client.get(
            reverse("reviews:review_create", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 302)

    def test_buyer_without_completed_order_cannot_create_review(self):
        self.completed_order.status = Order.Status.PENDING
        self.completed_order.save()
        self.client.force_login(self.buyer)
        response = self.client.get(
            reverse("reviews:review_create", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 403)

    def test_completed_buyer_can_create_one_review(self):
        self.client.force_login(self.buyer)
        url = reverse("reviews:review_create", args=[self.product.id])
        response = self.client.post(url, {"text": "Très bon produit", "rating": 5})
        self.assertRedirects(
            response,
            reverse("product_detail", args=[self.product.id]),
        )
        review = Review.objects.get(product=self.product, publier=self.buyer)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.text, "Très bon produit")

        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_whitespace_text_is_rejected(self):
        self.client.force_login(self.buyer)
        response = self.client.post(
            reverse("reviews:review_create", args=[self.product.id]),
            {"text": "   ", "rating": 4},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(product=self.product).exists())

    def test_owner_can_update_review_but_other_user_cannot(self):
        review = Review.objects.create(
            product=self.product,
            publier=self.buyer,
            text="Avant",
            rating=3,
        )
        url = reverse("reviews:review_update", args=[review.id])

        self.client.force_login(self.other)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.force_login(self.buyer)
        response = self.client.post(url, {"text": "Après", "rating": 5})
        self.assertRedirects(
            response,
            reverse("product_detail", args=[self.product.id]),
        )
        review.refresh_from_db()
        self.assertEqual(review.text, "Après")
        self.assertEqual(review.rating, 5)

    def test_model_prevents_rating_outside_one_to_five(self):
        review = Review(
            product=self.product,
            publier=self.buyer,
            text="Avis",
            rating=6,
        )
        with self.assertRaises(ValidationError):
            review.full_clean()
