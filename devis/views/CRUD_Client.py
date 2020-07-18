from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from devis.models import Client


@method_decorator(login_required, name='dispatch')
class ListeClients(ListView):
    model = Client
    context_object_name = "clients"
    template_name = "devis/client_list.html"
    paginate_by = 10

    def get_queryset(self):
        result = super(ListeClients, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Client.objects.filter(
                Q(intitule__icontains=query) | Q(telephone__icontains=query) | Q(adresse__icontains=query) | Q(
                    complement_adresse__icontains=query))
            result = postresult
        return result


@method_decorator(login_required, name='dispatch')
class ClientCreate(CreateView):
    model = Client
    template_name = "devis/client_creer.html"
    fields = ['intitule', 'adresse', 'complement_adresse', 'telephone']
    success_url = reverse_lazy("liste_clients")

    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Client ajouté avec succès !")

        if self.request.session.get("ajout_client_inconnu_pour_devis", None):
            self.request.session["client"] = {
                'intitule': self.object.intitule,
                'id': self.object.id
            }
            return redirect("sauvegarder_devis")

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required, name='dispatch')
class ClientUpdate(UpdateView):
    model = Client
    fields = ['intitule', 'adresse', 'complement_adresse', 'telephone']
    template_name = "devis/client_update.html"


@method_decorator(login_required, name='dispatch')
class ClientDetail(DetailView):
    context_object_name = "client"
    model = Client
    template_name = "devis/client_detail.html"
