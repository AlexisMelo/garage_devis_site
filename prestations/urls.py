from django.urls import path
from django.contrib.auth import views as auth_views

from prestations import views

urlpatterns = [
    path('cout_fixe/', views.ListePrestationCoutFixe.as_view(), name="liste_prestations_cout_fixe"),
    path('cout_variable/', views.ListePrestationCoutVariable.as_view(), name="liste_prestations_cout_variable"),
    path('',views.gestion_prestations_choix, name="gestion_choix_prestation"),
    path('cout_fixe/ajout', views.CreatePrestationCoutFixe.as_view(), name="ajout_prestation_cout_fixe")
]
