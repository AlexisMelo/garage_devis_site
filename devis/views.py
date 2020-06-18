# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from devis.models import Devis, Client, Prestation
from .forms import PrestationAjoutForm, DevisAjoutForm, DevisModifForm


# Create your views here.

def oral_ecrit(request):
    return render(request, 'devis/oral_ecrit.html')


def liste_devis(request):
    devis = Devis.objects.all()
    ajout = request.session.get('ajout', None)
    modif = request.session.get('modif', None)
    if ajout:
        del request.session['ajout']
    if modif:
        del request.session['modif']
    return render(request, 'devis/liste_devis.html', {'devis': devis, 'ajout': ajout, 'modif': modif})


def devis_from_list(request, numeroDevis):
    devis = get_object_or_404(Devis, id=numeroDevis)
    return render(request, 'devis/devis_full.html', {'devis': devis})


def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'devis/liste_clients.html', {'clients': clients})


def liste_prestations(request):
    prest = Prestation.objects.all()
    return render(request, 'devis/liste_prestations.html', {'prestations': prest})


def creer_prestation_formulaire(request):
    form = PrestationAjoutForm(request.POST or None)

    if form.is_valid():
        prix = form.cleaned_data["prix"]
        titre = form.cleaned_data["titre"]

        prestation = Prestation(prix=prix, titre=titre)
        prestation.save()

        ajout_valid = True

    return render(request, 'devis/creer_prestation_formulaire.html', locals())


def creer_devis_formulaire(request):

    form = DevisAjoutForm(request.POST or None)

    if form.is_valid():
        form.save()
        ajout = True

        request.session['ajout'] = True
        return redirect('liste_devis')

    return render(request, 'devis/creer_devis_formulaire.html', locals())

def modifier_devis_formulaire(request, numeroDevis):
    devis = get_object_or_404(Devis,id=numeroDevis)

    form = DevisModifForm(request.POST or None, instance=devis)

    if form.is_valid():
        nouveauDevis = form.save(commit=False)

        nouveauDevis.prestations.set(form.cleaned_data["prestations"])
        nouveauDevis.save()

        request.session['modif'] = True
        return redirect('liste_devis')

    return render(request, 'devis/edit_devis_formulaire.html', locals())