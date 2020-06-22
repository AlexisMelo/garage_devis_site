from django.conf.urls import url
from django.urls import path
from django.views.generic import ListView

from . import views
from .models import Client

urlpatterns = [
    path('choix/', views.oral_ecrit, name="creer_devis"),
    path('', views.ListeDevis.as_view(), name="liste_devis"),
    path('clients/', views.ListeClients.as_view(), name="liste_clients"),
    path('prestation/', views.ListePrestation.as_view(), name="liste_prestations"),
    path('<pk>', views.DevisDetail.as_view(), name="devis_detail"),
    path('modifier/<pk>', views.DevisUpdate.as_view(), name="edit_devis"),
    path('ajout/', views.DevisCreate.as_view(), name="ajout_devis"),
    path('oral/', views.devis_pneu_oral, name="devis_pneu_oral"),
    path('ecrit/',views.devis_creation_ecrit, name="devis_creation_ecrit"),
    path('ajouter/prestation_cout_fixe', views.ajouter_prestation_cout_fixe, name="ajouter_prestation_cout_fixe")
]
