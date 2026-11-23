from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from orders.models import Order
from products.models import Product

from .forms import LoginForm, RegisterForm
from django.contrib import messages
from .models import OTPVerification
from .utils import send_otp_via_brevo

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            whatsapp = form.cleaned_data['whatsapp_number']
            
            # Sécurité : Nettoie les anciens comptes inactifs avec le même numéro/email
            User.objects.filter(whatsapp_number=whatsapp, is_active=False).delete()
            User.objects.filter(email=email, is_active=False).delete()
            
            # 1. Créer l'utilisateur mais INACTIF en attendant la vérification
            user = form.save(commit=False)
            user.is_active = False 
            user.save()

            # 2. Générer et envoyer l'OTP par email
            otp_record = OTPVerification.generate_otp(user.email)
            send_otp_via_brevo(user.email, otp_record.otp_code)

            # 3. Stocker l'ID en session pour l'étape suivante
            request.session['pending_user_id'] = user.id
            messages.info(request, "Un code de vérification a été envoyé à votre adresse email.")
            return redirect("verify_otp")
    else:
        form = RegisterForm()
    
    return render(request, "accounts/register.html", {"form": form})


def _safe_next_url(request):
    """Renvoie l'URL "next" seulement si elle pointe vers ce site (anti open-redirect)."""
    next_url = request.POST.get("next") or request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(_safe_next_url(request) or "dashboard")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    orders = Order.objects.select_related("product__seller", "buyer")

    # Mes annonces en ligne
    products = Product.objects.filter(seller=user, is_active=True).select_related("category")
    # Les commandes que j'ai faites (en attente)
    purchases = orders.filter(buyer=user, status=Order.Status.PENDING)
    # Les commandes que j'ai reçues (en attente)
    received_orders = orders.filter(product__seller=user, status=Order.Status.PENDING)
    # Mes ventes terminées
    sales = orders.filter(product__seller=user, status=Order.Status.COMPLETED)
    # Mes achats terminés
    boughts = orders.filter(buyer=user, status=Order.Status.COMPLETED)

    return render(
        request,
        "accounts/dashboard.html",
        {
            "products": products,
            "boughts": boughts,
            "received_orders": received_orders,
            "purchases": purchases,
            "sales": sales,
        },
    )


def logout_view(request):
    logout(request)
    return redirect("login")

def verify_otp(request):
    pending_user_id = request.session.get('pending_user_id')
    if not pending_user_id:
        return redirect("register")

    try:
        user = User.objects.get(id=pending_user_id)
    except User.DoesNotExist:
        return redirect("register")

    if request.method == "POST":
        # Formulaire simple pour le code (à créer dans forms.py si vous préférez, ou inline ici)
        otp_code = request.POST.get('otp_code', '').strip()
        
        otp_record = OTPVerification.objects.filter(
            email=user.email,
            otp_code=otp_code,
            is_verified=False
        ).first()

        if otp_record and otp_record.is_valid():
            # Code valide !
            otp_record.is_verified = True
            otp_record.save()
            
            # Activer le compte
            user.is_active = True
            user.save()
            
            # Nettoyer la session et connecter l'utilisateur
            del request.session['pending_user_id']
            login(request, user)
            messages.success(request, "Compte vérifié avec succès ! Bienvenue.")
            return redirect("dashboard") # Adaptez si votre page d'accueil s'appelle autrement
        else:
            messages.error(request, "Code invalide ou expiré. Veuillez vérifier votre email ou demander un nouveau code.")
    
    return render(request, "accounts/verify_otp.html", {"email": user.email})
