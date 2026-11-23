from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, whatsapp_number, password=None, **extra_fields):
        if not whatsapp_number:
            raise ValueError("Le numéro WhatsApp est obligatoire.")
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        
        whatsapp_number = self.normalize_whatsapp(whatsapp_number)
        email = self.normalize_email(email)
        
        user = self.model(whatsapp_number=whatsapp_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, whatsapp_number,email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Un superutilisateur doit avoir is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Un superutilisateur doit avoir is_superuser=True")
        return self.create_user(whatsapp_number, password, **extra_fields)

    @staticmethod
    def normalize_whatsapp(number):
        return "".join(c for c in number if c.isdigit() or c == "+")


class User(AbstractUser):
    username = None
    email = models.EmailField("adresse email", unique=True, blank=False, null=False)
    first_name = models.CharField("prénom", max_length=150)
    last_name = models.CharField("nom", max_length=150)
    whatsapp_number = models.CharField(
        "numéro WhatsApp",
        max_length=16,
        unique=True,
        validators=[
            RegexValidator(
                r"^\+\d{8,15}$",
                "Format international requis, ex : +22997000000",
            )
        ],
    )

    USERNAME_FIELD = "whatsapp_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    objects = UserManager()

    @property
    def whatsapp_link(self):
        return f"https://wa.me/{self.whatsapp_number.lstrip('+')}"     


class OTPVerification(models.Model):
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_valid(self):
        
        expiration_time = self.created_at + timedelta(minutes=10)
        return timezone.now() < expiration_time and not self.is_verified

    @classmethod
    def generate_otp(cls, email):
        cls.objects.filter(email=email, is_verified=False).delete()
        code = str(random.randint(100000, 999999))
        return cls.objects.create(email=email, otp_code=code)