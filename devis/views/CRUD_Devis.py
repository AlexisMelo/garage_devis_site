from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from devis.forms import DevisModifForm, DevisAjoutForm
from devis.models import Devis


@method_decorator(login_required, name='dispatch')
class ListeDevis(ListView):
    model = Devis
    context_object_name = "devis"
    template_name = "devis/devis_list.html"
    paginate_by = 10


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
class DevisDetail(DetailView):
    context_object_name = "devis"
    model = Devis
    template_name = "devis/devis_detail.html"
