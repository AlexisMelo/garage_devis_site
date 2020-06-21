from django.urls import path

from utilisateurs import views

urlpatterns = [
    path('connexion/',views.connexion, name="connexion"),
    path('deconnexion/',views.deconnexion, name="deconnexion"),
]
