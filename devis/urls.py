from django.urls import path
from . import views

urlpatterns = [
    path('choix/', views.oral_ecrit, name="creer_devis"),
    path('liste_devis/', views.liste_devis, name="liste_devis"),
    path('liste_clients/', views.liste_clients, name="liste_clients"),
    path('liste_prestations/', views.liste_prestations, name="liste_prestations"),
    path('liste/<numeroDevis>', views.devis_from_list, name="devis_unique"),
]
