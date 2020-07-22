from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.generic import ListView

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