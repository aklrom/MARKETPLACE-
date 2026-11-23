import requests
from django.conf import settings

def send_otp_via_brevo(email: str, otp_code: str) -> bool:
    """
    Envoie l'OTP via l'API Transactionnelle de Brevo (Gratuit : 300 emails/jour).
    """
    api_key = getattr(settings, 'BREVO_API_KEY', '')
    
    # Mode développement : si pas de clé, on affiche le code dans la console
    if not api_key:
        print(f"⚠️ [DEV] Clé Brevo manquante. Code OTP généré pour {email} : {otp_code}")
        return True

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }
    
    # Remplacez par l'email expéditeur vérifié dans votre compte Brevo
    sender_email = getattr(settings, 'BREVO_SENDER_EMAIL', 'noreply@votre-domaine.com')
    sender_name = getattr(settings, 'BREVO_SENDER_NAME', 'MARKETPLACE')

    data = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": email}],
        "subject": "🔒 Votre code de vérification MARKETPLACE",
        "htmlContent": f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px;">
            <h2 style="color: #333;">Vérification de votre compte</h2>
            <p>Bonjour,</p>
            <p>Pour finaliser votre inscription sur MARKETPLACE, veuillez utiliser le code de vérification suivant :</p>
            <h1 style="color: #007bff; letter-spacing: 5px; text-align: center; background: #f4f4f4; padding: 15px; border-radius: 5px;">{otp_code}</h1>
            <p>Ce code est valable <strong>10 minutes</strong>. Ne le partagez avec personne.</p>
            <p>Si vous n'êtes pas à l'origine de cette demande, ignorez simplement cet email.</p>
            <br>
            <p style="color: #777; font-size: 12px;">L'équipe MARKETPLACE</p>
        </div>
        """
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur d'envoi Brevo : {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Détails : {e.response.text}")
        return False