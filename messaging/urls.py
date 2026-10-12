from django.urls import path
from . import views

urlpatterns=[
    path("",views.dm_list,name="conversation_list"),
    path("conversation/<int:id>/",views.get_messages,name="get_messages"),
    path("conversation_json/<int:id>/",views.get_messages_json,name="get_messages_json")
]