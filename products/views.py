from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product
from django.shortcuts import redirect ,render
from .forms import ProductForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

def product_list(request):
    products=Product.objects.all()

    return render(request,"products/product_list.html",{"products":products})


def product_detail(request,id):
    product=Product.objects.get(id=id)
    return render(request,"products/product_detail.html",{"product":product})

@login_required
def product_create(request):
    if request.method=="POST":
        form=ProductForm(request.POST)

        if form.is_valid():
            product=form.save(commit=False)
            product.seller=request.user
            product.save()

            return redirect("product_detail", id=product.id)
    else:
        form=ProductForm()

    return render(request,"products/product_form.html",{"form":form})        

@login_required
def product_update(request, id):
    product = get_object_or_404(Product, id=id)

    # Vérification de propriété
    if product.seller != request.user:
        return HttpResponseForbidden(
            "Vous n'avez pas le droit de modifier ce produit."
        )

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            form.save()
            return redirect("product_detail", id=product.id)

    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/product_form.html",
        {
            "form": form,
            "title": "Modifier le produit"
        }
    )

@login_required
def product_delete(request,id):
    product=get_object_or_404(Product,id=id)

    if product.seller!=request.user:
        return HttpResponseForbidden("Vous ne pouver pas supprimer cet article")

    if request.method == "POST":
        product.delete()
        return redirect("product_list")

    return render(request,"products/product_confirm_delete.html",{"product":product})
# Create your views here.
