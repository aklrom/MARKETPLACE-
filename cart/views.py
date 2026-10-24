from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from orders.models import Order
from products.models import Product


class CheckoutError(Exception):
    """Erreur affichable à l'acheteur ; annule toute la transaction."""


def _error(request, message, status=400):
    return render(request, "cart/cart_error.html", {"message": message}, status=status)


def _get_cart(request):
    return request.session.get("cart", {})


def _save_cart(request, cart):
    request.session["cart"] = cart


def _cart_quantities(cart):
    """Convertit {"12": 2} en {12: 2}, en ignorant les entrées invalides."""
    result = {}
    for key, qty in cart.items():
        try:
            product_id, quantity = int(key), int(qty)
        except (TypeError, ValueError):
            continue
        if quantity >= 1:
            result[product_id] = quantity
    return result


@login_required
@require_POST
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id, is_active=True)

    if product.seller_id == request.user.id:
        return _error(request, "Vous ne pouvez pas acheter votre propre produit.")

    cart = _get_cart(request)
    key = str(product.id)
    new_quantity = cart.get(key, 0) + 1

    if new_quantity > product.quantity:
        return _error(request, "Stock insuffisant pour ajouter ce produit.")

    cart[key] = new_quantity
    _save_cart(request, cart)
    messages.success(request, "Produit ajouté au panier.")
    return redirect("product_detail", id=product.id)


@login_required
@require_POST
def increase_quantity(request, id):
    cart = _get_cart(request)
    key = str(id)

    if key not in cart:
        return _error(request, "Ce produit n'est pas dans le panier.")

    product = get_object_or_404(Product, id=id, is_active=True)

    if cart[key] + 1 > product.quantity:
        return _error(request, "Vous ne pouvez pas en commander davantage.")

    cart[key] += 1
    _save_cart(request, cart)
    return redirect("cart")


@login_required
@require_POST
def decrease_quantity(request, id):
    cart = _get_cart(request)
    key = str(id)

    if key not in cart:
        return _error(request, "Ce produit n'est pas dans le panier.")

    if cart[key] > 1:
        cart[key] -= 1
    else:
        del cart[key]

    _save_cart(request, cart)
    return redirect("cart")


@login_required
@require_POST
def delete_product_in_cart(request, id):
    cart = _get_cart(request)
    key = str(id)

    if key not in cart:
        return _error(request, "Ce produit n'est pas dans le panier.")

    del cart[key]
    _save_cart(request, cart)
    return redirect("cart")


@login_required
def cart_detail(request):
    quantities = _cart_quantities(_get_cart(request))
    if not quantities:
        return redirect("product_list")

    products = Product.objects.in_bulk(list(quantities))
    cart_list = []
    sous_a_payer = Decimal("0")

    for product_id, quantity in quantities.items():
        product = products.get(product_id)
        if product is None:
            continue

        problem = ""
        if not product.is_active:
            problem = "Ce produit n'est plus en vente."
        elif product.quantity < 1:
            problem = "Ce produit est épuisé."
        elif product.quantity < quantity:
            problem = f"Stock insuffisant : il en reste {product.quantity}."

        sous_total = product.price * quantity
        if not problem:
            sous_a_payer += sous_total

        cart_list.append({
            "name": product.name,
            "id": product.id,
            "quantity": quantity,
            "sous_total": sous_total,
            "price": product.price,
            "problem": problem,
        })

    if not cart_list:
        return redirect("product_list")

    return render(
        request,
        "cart/cart.html",
        {
            "cart_list": cart_list,
            "sous_a_payer": sous_a_payer,
            "has_problem": any(line["problem"] for line in cart_list),
        },
    )


@login_required
@require_POST
def checkout(request):
    quantities = _cart_quantities(_get_cart(request))
    if not quantities:
        return redirect("product_list")

    try:
        with transaction.atomic():
            # Verrou des produits, toujours dans le même ordre (évite les blocages
            # entre deux paiements simultanés).
            products = {
                product.id: product
                for product in Product.objects.select_for_update()
                .filter(id__in=list(quantities))
                .order_by("id")
            }

            for product_id in sorted(quantities):
                quantity = quantities[product_id]
                product = products.get(product_id)

                if product is None or not product.is_active:
                    raise CheckoutError(
                        "Un produit de votre panier n'est plus disponible."
                    )
                if product.seller_id == request.user.id:
                    raise CheckoutError(
                        f"Vous ne pouvez pas acheter votre propre produit : {product.name}."
                    )
                if product.quantity < quantity:
                    raise CheckoutError(
                        f"Il ne reste que {product.quantity} de {product.name}."
                    )

                # Décrément conditionnel : sûr même si le verrou n'existe pas (SQLite).
                updated = Product.objects.filter(
                    pk=product_id, quantity__gte=quantity
                ).update(
                    quantity=F("quantity") - quantity,
                    updated_at=timezone.now(),
                )
                if not updated:
                    raise CheckoutError(f"Stock insuffisant pour {product.name}.")

                Order.objects.create(
                    buyer=request.user,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price,  # toujours copié depuis le produit
                )
    except CheckoutError as exc:
        return _error(request, str(exc), status=409)

    _save_cart(request, {})
    messages.success(request, "Votre commande a bien été enregistrée.")
    return redirect("dashboard")

