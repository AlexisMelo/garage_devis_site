from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from prestations.forms import CreatePrestationCoutFixeForm
from prestations.models import PrestationCoutFixe

@method_decorator(login_required, name='dispatch')
class ListePrestationCoutFixe(ListView):
    model = PrestationCoutFixe
    context_object_name = "prestations"
    template_name = "prestations/prestation_cout_fixe_list.html"
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class CreatePrestationCoutFixe(CreateView):
    model = PrestationCoutFixe
    template_name = "prestations/prestation_cout_fixe_creer.html"
    form_class = CreatePrestationCoutFixeForm
    success_url = reverse_lazy("liste_prestations_cout_fixe")

    def get_initial(self):
        return {
            'libelle' : None,
            'categorie': "Sélectionnez une catégorie"
        }
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Forfait ajouté avec succès !")

        return HttpResponseRedirect(self.get_success_url())