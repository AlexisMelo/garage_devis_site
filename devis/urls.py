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
    path('<int:pk>', views.DevisDetail.as_view(), name="devis_detail"),
    path('clients/<int:pk>', views.ClientDetail.as_view(), name="client_detail"),
    path('clients/ajout', views.ClientCreate.as_view(), name="ajout_client"),
    path('clients/update/<int:pk>', views.ClientUpdate.as_view(), name="update_client"),
    path('oral/', views.ajouter_prestation_pneumatique, name="devis_pneu_oral"),
    path('ajouter/prestation_mecanique', views.ajouter_prestation_mecanique, name="ajouter_prestation_mecanique"),
    path('nouveau/',views.devis_creation_ecrit, name="devis_creation_ecrit"),
    path('nouveau/depuis_client/<int:numClient>', views.ajouter_client_en_session_avec_id, name="nouveau_devis_depuis_client"),
    path('reset/',views.reset, name="reset"),
    path('<int:pk>/pdf/', views.generer_pdf, name="get_pdf"),
    path('ajouter/prestation_pneumatique_en_session', views.ajouter_prestation_pneumatique_en_session, name="ajouter_prestation_pneumatique_en_session"),
    path('ajouter/prestation_cout_fixe_en_session', views.ajouter_prestation_fixe_en_session, name="ajouter_prestation_fixe_en_session"),
    path('ajouter/prestation_cout_variable_en_session', views.ajouter_prestation_variable_en_session, name="ajouter_prestation_variable_en_session"),
    path('ajouter/prestation_nvelle_session', views.ajouter_prestation_nouvelle_en_session, name="ajouter_prestation_nouvelle_en_session"),
    path('ajouter/ajouter_client_en_session', views.ajouter_client_en_session, name="ajouter_client_en_session"),
    path('ajouter/mo_en_session', views.ajouter_mo_session, name="ajouter_mo_en_session"),
    path('supprimer/prestation_en_session/<str:type_prestation>/<str:prestation_id>)', views.supprimer_prestation_en_session, name="supprimer_prestation_en_session"),
    path('sauvegarder/', views.sauvegarder_devis, name="sauvegarder_devis"),
]
