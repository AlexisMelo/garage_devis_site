from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render
from django.urls import reverse

from devis.models import Client, Categorie, PrestationCoutFixe, PrestationCoutVariableStandard, Devis


def devis_pneu_oral(request):
    if request.META.get('HTTP_REFERER').endswith(reverse('devis_creation_ecrit')):
        ajout_au_devis_possible = True

    return render(request, 'devis/devis_pneu_oral.html', locals())


@login_required
def devis_creation_ecrit(request):
    if not 'devis_en_creation' in request.session:
        request.session['devis_en_creation'] = True

    allClients = Client.objects.all()
    jsonClients = serializers.serialize('json', allClients)

    if request.session['devis_en_creation']:

        tousMesDevis = Devis.objects.all()
        nbDevis = tousMesDevis.count()
        numeroSupposeDevis = 1
        if nbDevis != 0:
            numeroSupposeDevis = tousMesDevis.aggregate(Max('id'))['id__max'] + 1
        request.session['numeroProchainDevis'] = numeroSupposeDevis

        if 'mesPrestationsCoutFixe' in request.session:
            # afficher prestations
            mesPrestationsCoutFixe = request.session['mesPrestationsCoutFixe']

    return render(request, 'devis/devis_creation_ecrit.html', locals())

@login_required
def ajouter_prestation_cout_fixe(request):
    prestations = PrestationCoutFixe.objects.all()

    categoriesPossibles = prestations.values('categorie').distinct()

    categories = Categorie.objects.filter(id__in=categoriesPossibles)

    return render(request, 'devis/ajouter_prestation_cout_fixe.html', locals())

@login_required
def ajouter_prestation_cout_variable(request):
    prestations = PrestationCoutVariableStandard.objects.all()
    categoriesPossibles = prestations.values('categorie').distinct()
    categories = Categorie.objects.filter(id__in=categoriesPossibles)

    return render(request, 'devis/ajouter_prestation_cout_variable.html', locals())

