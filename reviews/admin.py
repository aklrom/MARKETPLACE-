from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "publier", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("text", "product__name", "publier__first_name", "publier__last_name")
