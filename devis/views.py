# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from devis.models import Devis, Client, Prestation

# Create your views here.

def oral_ecrit(request):
    return render(request, 'devis/oral_ecrit.html')

    # return HttpResponse("""
    # <h1>Outil de création de devis</h1>""")

def liste_devis(request):
    devis = Devis.objects.all()
    return render(request, 'devis/liste_devis.html', {'devis':devis})


def devis_from_list(request, numeroDevis):
    devis = get_object_or_404(Devis, id=numeroDevis)

    return render(request, 'devis/devis_full.html', {'devis': devis})

def liste_clients(request):
    clients = Client.objects.all()
    return render(request, 'devis/liste_clients.html', {'clients': clients})

def liste_prestations(request):
    prest = Prestation.objects.all()
    return render(request, 'devis/liste_prestations.html', {'prestations': prest})
