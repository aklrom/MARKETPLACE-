from django.urls import path
from . import views

urlpatterns=[
    path("",views.order_list,name="orders_list"),
    path("seller_status_confirm/<int:id>/", views.seller_status_confirm,name="seller_status_confirm"),
    path("buyer_status_confirm/<int:id>/", views.buyer_status_confirm,name="buyer_status_confirm"),
    path("cancel/<int:id>/", views.cancel_order, name="cancel_order"),
]