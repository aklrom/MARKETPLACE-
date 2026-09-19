from django.db import models
from django.contrib.auth import get_user_model
from orders.models import Order


User=get_user_model()

class Conversation(models.Model):

    order=models.OneToOneField(Order,on_delete=models.CASCADE,related_name="conversation")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['created_at']

    def __str__(self):
        return f'Conversation {self.order.buyer}--{self.order.product.seller}'

    

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE,related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['sent_at']

    def __str__(self):
        return f"De {self.sender} à {self.receiver}: {self.content[:30]}"
# Create your models here.
