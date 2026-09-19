from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_detail, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("increase/<int:id>/", views.increase_quantity, name="increase_quantity"),
    path("decrease/<int:id>/", views.decrease_quantity, name="decrease_quantity"),
    path("delete/<int:id>/", views.delete_product_in_cart, name="delete_product_in_cart"),
]