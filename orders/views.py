from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404,redirect,render
from django.http import HttpResponseForbidden
from products.models import Product
from .models import Order
from django.db import transaction
from messaging.models import Conversation


@login_required
def order_list(request):
    orders=Order.objects.filter(buyer=request.user)
    if not orders:
        orders="Aucune commande effectuées"
    return render(request,"orders/orders.html",{"orders":orders})


@login_required
def cancel_order(request,id):
    if request.method != "POST":
        return HttpResponseForbidden("Méthode non autorisée.")

    with transaction.atomic():
        order=get_object_or_404(Order,id=id)
        product=order.product

        if request.user not in [product.seller,order.buyer] or order.status!="pending":
            return HttpResponseForbidden(
                        "Vous n'avez pas le droit de gérer cette commande."
                    )
        if order.seller_status :
            return HttpResponseForbidden("Cette commande a déja été validée. Impossible de l'annuler.")
        order.status="cancelled"
        
        product.quantity+=order.quantity
        order.save()
        product.save()
        conversation=get_object_or_404(Conversation,order=order,is_deleted=False)
        conversation.is_deleted=True
        conversation.save()

    return redirect("dashboard")    

@login_required
def seller_status_confirm(request,id):
    
    if request.method!="POST":
        return HttpResponseForbidden("Mauvaise methode")
    order=get_object_or_404(Order,id=id)
    if order.status!="pending":
        return HttpResponseForbidden(
        "Cette commande ne peut pas encore être validée."
    )
    if request.user!=order.product.seller or order.seller_status:
        return HttpResponseForbidden("Vous n'etes pas autorisé à agir  ou  vous avez deja validé")
    with transaction.atomic():
        order.seller_status=True
        if order.seller_status and order.buyer_status:
            order.status="completed"
            conversation=Conversation.objects.get(order=order)
            conversation.is_deleted=True
            conversation.save()
        order.save()
    return redirect("dashboard")

@login_required
def buyer_status_confirm(request,id):
    if request.method!="POST":
        return HttpResponseForbidden("Mauvaise methode")
    order=get_object_or_404(Order,id=id)
    if  order.status!="pending":
        return HttpResponseForbidden(
        "Cette commande ne peut pas encore être validée."
    )
    if request.user!=order.buyer or order.buyer_status:
        return HttpResponseForbidden("Vous n'etes pas autorisé à agir ou vous avez deja confirmé")
    with transaction.atomic():
        order.buyer_status = True
        if order.seller_status and order.buyer_status:
            order.status = "completed"
            
            # Correction : Supprime la conversation de manière sécurisée si elle existe
            conversation=Conversation.objects.get(order=order)
            conversation.is_deleted=True
            conversation.save()
            
        order.save()

    return redirect("dashboard")

    


# Create your views here.
