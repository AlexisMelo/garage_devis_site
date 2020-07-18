from django.contrib import admin

# Register your models here.
from prestations.models import Marque, Categorie, Prestation, PrestationCoutVariableConcrete, PrestationCoutFixe, \
    PrestationCoutVariableStandard, PieceDetacheeStandard, PieceDetacheeAvecPrix, PrestationPneumatique, \
    PrestationMainOeuvre, PrestationNouvelle

admin.site.register(Marque)
admin.site.register(Categorie)
admin.site.register(Prestation)
admin.site.register(PrestationCoutVariableConcrete)
admin.site.register(PrestationCoutFixe)
admin.site.register(PrestationCoutVariableStandard)
admin.site.register(PieceDetacheeStandard)
admin.site.register(PieceDetacheeAvecPrix)
admin.site.register(PrestationPneumatique)
admin.site.register(PrestationMainOeuvre)
admin.site.register(PrestationNouvelle)