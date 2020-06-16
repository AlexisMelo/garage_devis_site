# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def oral_ecrit(request):
    return render(request, 'devis/oral_ecrit.html')

    # return HttpResponse("""
    # <h1>Outil de création de devis</h1>""")

def liste(request):
    return render(request, 'devis/liste_devis.html')


def devis_from_list(request, numeroDevis):
    return render(request, 'devis/devis_full.html', {'numeroDevis': numeroDevis})
