from __future__ import unicode_literals

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from utilisateurs.forms import ConnexionForm


def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
            else:
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'utilisateurs/connexion.html', locals())

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))