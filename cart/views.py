from django.shortcuts import render,get_object_or_404,redirect
from products.models import Product
from orders.models import Order
from django.db import transaction
from messaging.models import Conversation
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def add_to_cart(request,id):
    product = get_object_or_404(Product,id=id)
    cart = request.session.get("cart", {})
    product_id = str(product.id)
    if (cart.get(product_id,0)+1)>product.quantity or request.user==product.seller:
        return render(request,"cart/cart_error.html",{"message":"Vous ne pouvez pas acheter ce produit"})
    if product_id in cart:
        cart[product_id]+=1
    else:
        cart[product_id]=1

    request.session["cart"] = cart

    return redirect("product_detail",id =product.id) 

@login_required
def increase_quantity(request, id):
    cart = request.session.get("cart", {})

    product = get_object_or_404(Product, id=id)
    product_id = str(product.id)

    if product_id not in cart:
        return render(
            request,
            "cart/cart_error.html",
            {"message": "Ce produit n'est pas dans le panier"}
        )

    if cart[product_id] + 1 > product.quantity:
        return render(
            request,
            "cart/cart_error.html",
            {"message": "Vous ne pouvez pas en commander davantage"}
        )

    cart[product_id] += 1
    request.session["cart"] = cart

    return redirect("cart")


@login_required
def decrease_quantity(request, id):
    cart = request.session.get("cart", {})

    product = get_object_or_404(Product, id=id)
    product_id = str(product.id)

    if product_id not in cart:
        return render(
            request,
            "cart/cart_error.html",
            {"message": "Ce produit n'est pas dans le panier"}
        )

    if cart[product_id] > 1:
        cart[product_id] -= 1
    else:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")


@login_required
def delete_product_in_cart(request, id):
    cart = request.session.get("cart", {})

    product = get_object_or_404(Product, id=id)
    product_id = str(product.id)

    if product_id not in cart:
        return render(
            request,
            "cart/cart_error.html",
            {"message": "Ce produit n'est pas dans le panier"}
        )

    del cart[product_id]
    request.session["cart"] = cart

    return redirect("cart")

def cart_detail(request):
    cart=request.session.get(("cart"),{})
    if len(cart)==0:
        return redirect("product_list")
    cart_list=[]
    sous_a_payer=0
    for product_id in cart:
        product=get_object_or_404(Product,id=int(product_id))
        
        sous_total=product.price*cart.get(product_id)
        sous_a_payer+=sous_total
        cart_list.append({"name":product.name,"id":product.id,"quantity":cart.get(product_id),"sous_total":sous_total,"price":product.price})

    return render(request,"cart/cart.html",{"cart_list":cart_list,"sous_a_payer":sous_a_payer})    
@login_required
def checkout(request):
    if request.method=="POST":
        cart = request.session.get("cart", {})

        if len(cart) == 0:
            return redirect("product_list")

        products = []

        with transaction.atomic():

            # 1. Récupérer les produits et vérifier les stocks
            for product_id in cart:

                product = get_object_or_404(
                    Product.objects.select_for_update(),
                    id=int(product_id)
                )

                quantity = cart.get(product_id)

                if product.quantity < quantity:
                    return render(
                        request,
                        "cart/cart_error.html",
                        {
                            "message": (
                                f"Il ne reste que "
                                f"{product.quantity} de {product.name}"
                            )
                        }
                    )

                products.append({
                    "product": product,
                    "quantity": quantity
                })

            # 2. Modifier les stocks et créer les commandes
            for item in products:

                product = item["product"]
                quantity = item["quantity"]

                product.quantity -= quantity
                product.save()

                order=Order.objects.create(
                    buyer=request.user,
                    product=product,
                    quantity=quantity,
                    unit_price=product.price
                )
                
                Conversation.objects.create(order=order)
               

            # 3. Vider le panier
            request.session["cart"] = {}

    return redirect("dashboard")

