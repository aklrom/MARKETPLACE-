from django.db import models
from django.conf import settings


class Category(models.Model):
    name=models.CharField(max_length=100)
    description =models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    seller=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )    

    category=models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    name=models.CharField(max_length=200)
    description=models.TextField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    quantity=models.PositiveIntegerField(default=1)
    condition=models.CharField(max_length=50)
    status=models.CharField(max_length=20,default="active")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name



# Create your models here.
