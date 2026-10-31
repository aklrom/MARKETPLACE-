from django.db import models
from django.conf import settings
from products import Product

class Reviews():
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=False,related_name="review")
    product=models.ForeignKey(on_delete=models.CASCADE,related_name="review")
    text=models.TextField(related_name="review")
    rating=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.user==None: 
            return f" avis sur le {self.product}"
        else:
            return f"Avis de {self.user} sur {self.product}"
# Create your models here.
