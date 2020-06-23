# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Max
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
import json

from devis.models import Devis, Client, Prestation, PrestationCoutFixe, Categorie
from .forms import DevisAjoutForm, DevisModifForm


def oral_ecrit(request):
    return render(request, 'devis/devis_creation_oral_ecrit.html')


def devis_pneu_oral(request):
    return render(request, 'devis/devis_pneu_oral.html')


@login_required
def devis_creation_ecrit(request):
    if not 'devis_en_creation' in request.session:
        request.session['devis_en_creation'] = True

    allClients = Client.objects.all()
    jsonClients = serializers.serialize('json', allClients)

    if request.POST.get('client'):
        request.session['client'] = request.POST.get('client')
    elif 'client' not in request.session:
        request.session['client'] = False


    if request.session['devis_en_creation']:

        tousMesDevis = Devis.objects.all()
        nbDevis = tousMesDevis.count()

        numeroSupposeDevis = 1

        if nbDevis != 0:
            numeroSupposeDevis = tousMesDevis.aggregate(Max('id'))['id__max'] + 1

        request.session['numeroProchainDevis'] = numeroSupposeDevis

    return render(request, 'devis/devis_creation_ecrit.html', locals())

@method_decorator(login_required, name='dispatch')
class DevisUpdate(UpdateView):
    model = Devis
    template_name = "devis/devis_update.html"
    form_class = DevisModifForm
    success_url = reverse_lazy("liste_devis")

    def form_valid(self, form):
        self.object = form.save()

        messages.success(self.request, "Devis modifié avec succès !")
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class DevisCreate(CreateView):
    model = Devis
    template_name = "devis/devis_creer.html"
    form_class = DevisAjoutForm
    success_url = reverse_lazy("liste_devis")

    def form_valid(self, form):
        self.object = form.save()

        messages.success(self.request, "Devis créé avec succès !")
        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class ListeClients(ListView):
    model = Client
    context_object_name = "clients"
    template_name = "devis/client_list.html"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class ListePrestation(ListView):
    model = PrestationCoutFixe
    context_object_name = "prestations"
    template_name = "devis/prestation_list.html"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class ListeDevis(ListView):
    model = Devis
    context_object_name = "devis"
    template_name = "devis/devis_list.html"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class DevisDetail(DetailView):
    context_object_name = "devis"
    model = Devis
    template_name = "devis/devis_detail.html"

def ajouter_prestation_cout_fixe(request):

    prestations = PrestationCoutFixe.objects.all()

    categoriesPossibles = prestations.values('categorie').distinct()
    print(categoriesPossibles)

    categories = Categorie.objects.filter(id__in=categoriesPossibles)

    return render(request, 'devis/ajouter_prestation_cout_fixe.html', locals())
