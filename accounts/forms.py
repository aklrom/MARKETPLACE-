from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

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
        widget=forms.TextInput(attrs={"autofocus": True, "type": "tel", "class": "form-control"}),
    )

class RegisterForm(UserCreationForm):
    whatsapp_number = WhatsAppField(max_length=16, label="Numéro WhatsApp", widget=forms.TextInput(attrs={"class": "form-control", "type": "tel"}))
    email = forms.EmailField(label="Adresse email", widget=forms.EmailInput(attrs={"class": "form-control"}))
    
    class Meta:
        model = User
        fields = ("last_name", "first_name", "email", "whatsapp_number")