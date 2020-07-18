from django.shortcuts import render
from django.urls import reverse


def gestion_prestations_choix(request):
    return render(request, 'prestations/gestion_prestations_choix.html')


