from django.urls import path
from . import views

urlpatterns = [
    path('choix/', views.oral_ecrit, name="creer_devis"),
    path('liste/', views.liste, name="liste_devis"),
    path('liste/<numeroDevis>', views.devis_from_list, name="devis_unique"),
]
