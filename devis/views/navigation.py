from django.shortcuts import render
from django.urls import reverse


def oral_ecrit(request):
    return render(request, 'devis/devis_creation_oral_ecrit.html')


