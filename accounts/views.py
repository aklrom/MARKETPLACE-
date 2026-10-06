from django.shortcuts import redirect,render
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from products.models import Product
from orders.models import Order

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form=RegisterForm()    
    return render(request,"accounts/register.html",{"form":form})

def login_view(request):
    if request.method=="POST":
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect("dashboard")

    else:
        form=AuthenticationForm()

    return render(request,"accounts/login.html",{"form":form})     

@login_required
def dashboard(request):
    products=Product.objects.filter(seller=request.user,is_active=True) # annoncees
    purchases=Order.objects.filter(buyer=request.user,status="pending")# les commandes que j'ai faite
    received_orders=Order.objects.filter(product__seller=request.user,status="pending")# les commandes que j'ai reçu
    sales=Order.objects.filter(product__seller=request.user , status="completed")#mes ventes completées
    boughts=Order.objects.filter(buyer=request.user,status="completed")# mes achats
    return render(request,"accounts/dashboard.html",{"products":products,"boughts":boughts,"received_orders":received_orders,"purchases":purchases,"sales":sales}) 


def logout_view(request):
    logout(request)
    return redirect("login")
# Create your views here.
