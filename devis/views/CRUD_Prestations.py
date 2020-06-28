from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from devis.models import Prestation


@method_decorator(login_required, name='dispatch')
class ListePrestation(ListView):
    model = Prestation
    context_object_name = "prestations"
    template_name = "devis/prestation_list.html"
    paginate_by = 10
