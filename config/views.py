from django.shortcuts import render

from products.models import Product


def home(request):
    products = Product.objects.filter(
        is_active=True,
        quantity__gt=0,
    ).select_related("category")[:3]
    return render(request, "home.html", {"featured_products": products})
