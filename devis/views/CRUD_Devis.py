from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, UpdateView, CreateView, DetailView

from devis.models import Devis


@method_decorator(login_required, name='dispatch')
class ListeDevis(ListView):
    model = Devis
    context_object_name = "devis"
    template_name = "devis/devis_list.html"
    paginate_by = 10
    ordering = ['-id']

@method_decorator(login_required, name='dispatch')
class DevisDetail(DetailView):
    context_object_name = "devis"
    model = Devis
    template_name = "devis/devis_detail.html"
