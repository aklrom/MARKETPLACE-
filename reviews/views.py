from django.shortcuts import render, get_object_or_404, redirect
from .models import Review
from accounts.models import AbstractUser
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm 
from products.models import Product
from django.http import Http404,HttpResponseForbidden
from orders.models import Order
# Create your views here.

@login_required
def review_create(request,id):
    product=get_object_or_404(Product,id=id)
    has_purchased=Order.objects.filter(buyer=request.user,product=product,status=Order.Status.COMPLETED).exists()
    if not has_purchased:
        return HttpResponseForbidden("Vous ne pouvez pas laisser un avis sur ce produit car vous ne l'avez pas acheté.")
    if request.method=="POST":
        form= ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            product=get_object_or_404(Product,id=id)
            review= form.save(commit=False)
            review.product=product
            review.publier=request.user
            review.save()
            return redirect("product_detail", id=product.id)
    else:
        form=ReviewForm()
    return render(request,"products/product_form.html",{"subform":form,"subtitle": "Quelques avis sur le produit"})

@login_required
def review_update(request,id):
    review=get_object_or_404(Review,id=id)
    product=review.product
    if review.publier_id!= request.user.id:
        return HttpResponseForbidden("Vous n'avez pas le droit de modifier cet avis.")

    has_purchased=Order.objects.filter(buyer=request.user,product=product,status=Order.Status.COMPLETED).exists()
    if not has_purchased:
        return HttpResponseForbidden("Vous ne pouvez pas modifier cet avis car vous n'avez pas acheté ce produit.")
    if request.method=="POST":
        form=ReviewForm(request.POST, request.FILES, instance=review)
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

