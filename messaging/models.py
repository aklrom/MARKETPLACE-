from django.db import models
from django.conf import settings
from orders.models import Order
from django.core.exceptions import ValidationError

class Conversation(models.Model):

    order=models.OneToOneField(Order,on_delete=models.PROTECT,related_name="conversation")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return f'Conversation {self.order.buyer}--{self.order.product.seller}'

    

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.PROTECT,related_name="messages")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']
    @property
    def receiver(self):
        if self.sender == self.conversation.order.product.seller:
            return self.conversation.order.buyer 
        elif self.sender== self.conversation.order.buyer:
            return self.conversation.order.product.seller
        else :
            return None
    def clean(self):
        if self.sender not in [self.conversation.order.buyer,self.conversation.order.product.seller]:
            raise ValidationError(f"Vous n'etes pas autorisée à intervenir dans cette conversation {self.sender}")
        
    def __str__(self):
        return f"De {self.sender} à {self.receiver}: {self.content[:30]}"
# Create your models here.
