from django.urls import path
from . import views

urlpatterns = [
    path('choix/', views.oral_ecrit, name="creer_devis"),
    path('', views.liste_devis, name="liste_devis"),
    path('clients/', views.liste_clients, name="liste_clients"),
    path('prestation/', views.liste_prestations, name="liste_prestations"),
    path('liste/<numeroDevis>', views.devis_from_list, name="devis_unique"),
    path('prestation/ajout/',views.creer_prestation_formulaire, name="ajout_prestation"),
    path('modifier/<numeroDevis>', views.modifier_devis_formulaire, name="edit_devis"),
    path('ajout/', views.creer_devis_formulaire, name="ajout_devis")

]
