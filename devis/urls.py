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
    path('clients/ajout', views.ClientCreate.as_view(), name="ajout_client"),
    path('oral/', views.devis_pneu_oral, name="devis_pneu_oral"),
    path('ecrit/',views.devis_creation_ecrit, name="devis_creation_ecrit"),
    path('reset/',views.reset, name="reset"),
    path('ajouter/prestation_pneumatique_en_session', views.ajouter_prestation_pneumatique_en_session, name="ajouter_prestation_pneumatique_en_session"),
    path('ajouter/prestation_cout_fixe', views.ajouter_prestation_cout_fixe, name="ajouter_prestation_cout_fixe"),
    path('ajouter/prestation_cout_variable', views.ajouter_prestation_cout_variable, name="ajouter_prestation_cout_variable"),
    path('ajouter/prestation_cout_fixe_en_session', views.ajouter_prestation_fixe_en_session, name="ajouter_prestation_fixe_en_session"),
    path('ajouter/prestation_cout_variable_en_session', views.ajouter_prestation_variable_en_session, name="ajouter_prestation_variable_en_session"),
    path('ajouter/ajouter_client_en_session', views.ajouter_client_en_session, name="ajouter_client_en_session"),
    path('supprimer/prestation_en_session/<str:type_prestation>/<str:prestation_id>)', views.supprimer_prestation_en_session, name="supprimer_prestation_en_session"),
    path('sauvegarder/', views.sauvegarder_devis, name="sauvegarder_devis"),
]
