# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from devis.models import Devis, Client, Prestation, PrestationCoutFixe
from .forms import DevisAjoutForm, DevisModifForm


def oral_ecrit(request):
    return render(request, 'devis/devis_creation_oral_ecrit.html')


def devis_pneu_oral(request):
    return render(request, 'devis/devis_pneu_oral.html')


@login_required
def devis_creation_ecrit(request):
    return render(request, 'devis/devis_creation_ecrit.html')


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
    template_name = "client_list"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class ListePrestation(ListView):
    model = PrestationCoutFixe
    context_object_name = "prestations"
    template_name = "prestation_list"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class ListeDevis(ListView):
    model = Devis
    context_object_name = "devis"
    template_name = "devis_list"
    paginate_by = 10


@method_decorator(login_required, name='dispatch')
class DevisDetail(DetailView):
    context_object_name = "devis"
    model = Devis
    template_name = "devis/devis_detail.html"
