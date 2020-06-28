from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from devis.forms import ClientAjoutForm
from devis.models import Client


@method_decorator(login_required, name='dispatch')
class ListeClients(ListView):
    model = Client
    context_object_name = "clients"
    template_name = "devis/client_list.html"
    paginate_by = 10

@method_decorator(login_required, name='dispatch')
class ClientCreate(CreateView):
    model = Client
    template_name = "devis/client_creer.html"
    form_class = ClientAjoutForm
    success_url = reverse_lazy("liste_clients")
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, "Client ajouté avec succès !")
        return HttpResponseRedirect(self.get_success_url())
