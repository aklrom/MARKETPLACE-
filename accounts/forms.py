from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# ... WhatsAppField et RegisterForm restent identiques ...



class WhatsAppField(forms.CharField):
    """Nettoie le numéro (espaces, tirets...) avant la validation."""

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            value = User.objects.normalize_whatsapp(value)
        return value

class LoginForm(AuthenticationForm):
    username = WhatsAppField(
        label="Numéro WhatsApp",
        max_length=16,
        widget=forms.TextInput(attrs={"autofocus": True, "type": "tel"}),
    )
class RegisterForm(UserCreationForm):
    whatsapp_number = WhatsAppField(max_length=16, label="Numéro WhatsApp")

    class Meta:
        model = User
        fields = ("last_name", "first_name", "whatsapp_number")