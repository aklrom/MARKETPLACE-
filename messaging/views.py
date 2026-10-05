from django.contrib.auth.decorators import login_required
from .models import Conversation,Message
from django.shortcuts import get_object_or_404,redirect,render
from django.http import HttpResponseForbidden
from django.db import transaction
from orders.models import Order,Product
from django.db.models import Q

@login_required
def dm_list(request):
    orders=Order.objects.filter(Q(buyer=request.user)| Q(product__seller=request.user))
    if not orders:
        
        return render (request,"messaging/conversation_list.html",{"message":"Aucune conversation présente."})
    conversation_list=[]
    for order in orders:
        try:
            dm=Conversation.objects.get(order=order,is_deleted=False)
            buyer=dm.order.buyer
            seller=dm.order.product.seller
            if request.user not in [buyer,seller]:
                    return HttpResponseForbidden("Who are you neiger? Here is not for you")
            mate=buyer if request.user==seller else seller
            conversation_list.append({"mate":mate,"id":dm.id})
        except Conversation.DoesNotExist:
            pass
    
         
    if not conversation_list:
        return render (request,"messaging/conversation_list.html",{"message":"Aucune conversation pour l'instant"})
    return render (request,"messaging/conversation_list.html",{"conversation_list":conversation_list}) 

@login_required
def get_messages(request,id):
    dm=get_object_or_404(Conversation,id=id,is_deleted=False)
    buyer=dm.order.buyer
    seller=dm.order.product.seller
    if request.user not in [buyer,seller]:
            return HttpResponseForbidden("Who are you neiger? Here is not for you")
    if request.method=="POST":
        Message.objects.create(content=request.POST.get("message"),sender=request.user,conversation=dm)
    messages_exchanged=Message.objects.filter(conversation=dm)
        
    

    messages_all=[]
    for  message in messages_exchanged:
        messages_all.append({"content":message.content,"sent_at":message.sent_at,"sender":message.sender})
    

    return render (request,"messaging/conversation.html",{"message_all":messages_all})


