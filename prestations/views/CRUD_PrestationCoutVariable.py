from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView

from prestations.forms import CreatePrestationCoutVariableForm
from prestations.models import PrestationCoutVariableStandard, Categorie, PieceDetacheeStandard


@method_decorator(login_required, name='dispatch')
class ListePrestationCoutVariable(ListView):
    model = PrestationCoutVariableStandard
    context_object_name = "prestations"
    template_name = "prestations/prestation_cout_variable_list.html"
    paginate_by = 10
    ordering = 'libelle'

    def get_queryset(self):
        result = super(ListePrestationCoutVariable, self).get_queryset()
        query = self.request.GET.get('search')

        if query:
            catpossibles = Categorie.objects.filter(libelle__icontains=query).values_list('id', flat=True)
            print(catpossibles)

            piecesPossibles = PieceDetacheeStandard.objects.filter(libelle__icontains=query).values_list('id', flat=True)
            print(piecesPossibles)

            querycats = Q(libelle__icontains=query)
            querycats |= Q(categorie__id__in=catpossibles)
            querycats |= Q(pieces_detachees__id__in=piecesPossibles)

            postresult = PrestationCoutVariableStandard.objects.filter(querycats)

            result = postresult
        return result

@method_decorator(login_required, name='dispatch')
class CreatePrestationCoutVariable(CreateView):
    model = PrestationCoutVariableStandard
    template_name = "prestations/prestation_cout_variable_creer.html"
    form_class = CreatePrestationCoutVariableForm
    success_url = reverse_lazy("liste_prestations_cout_variable")

    def get_initial(self):
        return {
            'libelle' : None,
            'categorie': "Sélectionnez une catégorie"
        }
    def form_valid(self, form):
        print(form)
        self.object = form.save()
        print(self.object)
        messages.success(self.request, "Préstation à coût variable ajoutée avec succès !")

        return HttpResponseRedirect(self.get_success_url())