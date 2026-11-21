from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from .models import Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import ReviewForm
from products.models import Product
from django.http import HttpResponseForbidden
from orders.models import Order


def _has_completed_purchase(user, product):
    return Order.objects.filter(
        buyer=user,
        product=product,
        status=Order.Status.COMPLETED,
    ).exists()


@login_required
@require_http_methods(["GET", "POST"])
def review_create(request, id):
    product = get_object_or_404(Product, id=id)
    if Review.objects.filter(product=product, publier=request.user).exists():
        return HttpResponseForbidden("Vous avez déjà laissé un avis pour ce produit.")

    if not _has_completed_purchase(request.user, product):
        return HttpResponseForbidden("Vous ne pouvez pas laisser un avis sur ce produit car vous ne l'avez pas acheté.")
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.publier = request.user
            try:
                review.save()
            except IntegrityError:
                form.add_error(None, "Vous avez déjà laissé un avis pour ce produit.")
                return render(request, "reviews/review_form.html", {"form": form, "title": "Laisser un avis", "product": product})
            return redirect("product_detail", id=product.id)
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {"form": form, "title": "Laisser un avis", "product": product})


@login_required
@require_http_methods(["GET", "POST"])
def review_update(request, id):
    review = get_object_or_404(Review.objects.select_related("product", "publier"), id=id)
    product = review.product
    if review.publier_id != request.user.id:
        return HttpResponseForbidden("Vous n'avez pas le droit de modifier cet avis.")

    if not _has_completed_purchase(request.user, product):
        return HttpResponseForbidden("Vous ne pouvez pas modifier cet avis car vous n'avez pas acheté ce produit.")
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("product_detail", id=product.id)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/review_form.html",
        {"form": form, "title": "Modifier mon avis", "product": review.product}
    )  

