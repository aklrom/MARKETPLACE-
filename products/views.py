from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product
from orders.models import Order  # <--- AJOUT : Import du modèle Order pour la vérification


def product_list(request):
    products = Product.objects.filter(
        is_active=True,
        quantity__gt=0,
    ).select_related("category", "seller")
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, id):
    product = get_object_or_404(
        Product.objects.select_related("category", "seller"),
        id=id,
    )
    # Un article retiré de la vente n'est visible que par son vendeur.
    if not product.is_active and product.seller_id != request.user.id:
        raise Http404

    # --- NOUVEAU : Vérification du droit d'avis ---
    can_review = False
    if request.user.is_authenticated:
        can_review = Order.objects.filter(
            buyer=request.user,
            product=product,
            status=Order.Status.COMPLETED  # On vérifie que la commande est bien terminée
        ).exists()
    # ----------------------------------------------

    return render(
        request, 
        "products/product_detail.html", 
        {
            "product": product,
            "can_review": can_review,  # <--- AJOUT : On passe cette variable au template
        }
    )


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("product_detail", id=product.id)
    else:
        form = ProductForm()

    return render(
        request,
        "products/product_form.html",
        {"form": form, "title": "Publier un produit"},
    )


@login_required
def product_update(request, id):
    product = get_object_or_404(Product, id=id)

    if product.seller_id != request.user.id:
        return HttpResponseForbidden("Vous n'avez pas le droit de modifier ce produit.")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("product_detail", id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/product_form.html",
        {"form": form, "title": "Modifier le produit"},
    )


@login_required
def product_delete(request, id):
    product = get_object_or_404(Product, id=id)

    if product.seller_id != request.user.id:
        return HttpResponseForbidden("Vous ne pouvez pas supprimer cet article.")

    if request.method == "POST":
        # Suppression douce : l'historique des commandes reste intact.
        product.is_active = False
        product.save(update_fields=["is_active", "updated_at"])
        return redirect("product_list")

    return render(request, "products/product_confirm_delete.html", {"product": product})