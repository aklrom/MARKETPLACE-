from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import Order


@login_required
def order_list(request):
    orders = Order.objects.filter(buyer=request.user).select_related("product__seller")
    return render(request, "orders/orders.html", {"orders": orders})


def _run_action(action, order_id, user):
    """Exécute une action sur une commande et traduit les erreurs en réponses HTTP."""
    try:
        action(order_id, user)
    except Order.DoesNotExist:
        raise Http404("Commande introuvable.")
    except PermissionDenied as exc:
        return HttpResponseForbidden(str(exc))
    return redirect("dashboard")


@login_required
@require_POST
def cancel_order(request, id):
    return _run_action(Order.cancel_by, id, request.user)


@login_required
@require_POST
def seller_status_confirm(request, id):
    return _run_action(Order.confirm_as_seller, id, request.user)


@login_required
@require_POST
def buyer_status_confirm(request, id):
    return _run_action(Order.confirm_as_buyer, id, request.user)