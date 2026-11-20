from django.db import models
from django.conf import settings
from products.models import Product

class Review(models.Model):
    publier=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="review")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="reviews")
    text=models.TextField()
    rating=models.IntegerField(choices=[(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5")])
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.user==None: 
            return f" avis sur le {self.product}"
        else:
            return f"Avis de {self.publier} sur {self.product}"
# Create your models here.
