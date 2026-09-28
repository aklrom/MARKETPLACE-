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
        
        return render (request,"messaging/conversation.html",{"message":"Aucune conversation présente."})
    conversation_list=[]
    for order in orders:
        try:
            conversation_list.append(Conversation.objects.get(order=order))
        except:
            pass    
    if not conversation_list:
        return render (request,"messaging/conversation_list.html",{"message":"Aucune conversation pour l'instant"})
    return render (request,"messaging/conversation_list.html",{"conversaion_list":conversation_list}) 

@login_required
def get_conversation(request,message_id):
    
    messages_exchanged=Message.objects.filter(id=message_id)

    if request.method=="POST":
        message=Message.objects.get(id=message_id)
        new_message=Message.create(content=request.POST.get("content"),sender=request.user,conversation=message.conversation)
        new_message.save()


    return render (request,"messaging/conversation.html",{"message_send":messages_exchanged})

#1 lister  les conversation de l'user connected
#2vue pour affficher une conversation et envoyer un nouveau message
