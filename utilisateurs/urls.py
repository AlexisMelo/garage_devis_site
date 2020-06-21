from django.urls import path
from django.contrib.auth import views as auth_views

from utilisateurs import views

urlpatterns = [
    path('connexion/',views.connexion, name="connexion"),
    path('deconnexion/',views.deconnexion, name="deconnexion"),
]
