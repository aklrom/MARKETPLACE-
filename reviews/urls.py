# reviews/urls.py
from django.urls import path
from . import views

app_name = 'reviews' # Bonne pratique pour l'espacement de noms (namespacing)

urlpatterns = [
    # URL pour créer un avis sur un produit spécifique
    # Correspond à {% url 'review_create' product.id %} dans le template
    path(
        'product/<int:id>/review/create/', 
        views.create_review, 
        name='review_create'
    ),
    
    # URL pour modifier un avis existant
    # Correspond à {% url 'review_update' review.id %} dans le template
    path(
        'review/<int:id>/update/', 
        views.review_update, 
        name='review_update'
    ),
]