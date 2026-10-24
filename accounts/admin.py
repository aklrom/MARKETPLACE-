from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .forms import RegisterForm
from .models import User


class UserAdminChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    form = UserAdminChangeForm
    add_form = RegisterForm  # réutilise ton formulaire d'inscription

    ordering = ("last_name", "first_name")
    list_display = ("whatsapp_number", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("whatsapp_number", "first_name", "last_name")

    fieldsets = (
        (None, {"fields": ("whatsapp_number", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name")}),
        ("Permissions", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("whatsapp_number", "first_name", "last_name", "password1", "password2"),
        }),
    )