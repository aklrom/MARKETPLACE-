import os
import django

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

# Récupération des variables d'environnement
whatsapp_number = os.getenv('DJANGO_SUPERUSER_WHATSAPP', '+22997000000') # Format: +229XXXXXXXX
first_name = os.getenv('DJANGO_SUPERUSER_FIRST_NAME', 'Admin')
last_name = os.getenv('DJANGO_SUPERUSER_LAST_NAME', 'Marketplace')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'AdminPassword123!')

# Vérifie si l'admin existe déjà pour éviter les erreurs
if not User.objects.filter(whatsapp_number=whatsapp_number).exists():
    User.objects.create_superuser(
        whatsapp_number=whatsapp_number,
        first_name=first_name,
        last_name=last_name,
        password=password
    )
    print(f"✅ Superutilisateur '{whatsapp_number}' créé avec succès en production !")
else:
    print(f"ℹ️ Le superutilisateur '{whatsapp_number}' existe déjà.")