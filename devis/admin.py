# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Devis, Client, Prestation, PrestationCoutVariableConcrete, PrestationCoutFixe, \
    PrestationCoutVariableStandard, PieceDetacheeStandard, PieceDetacheeAvecPrix, Categorie, Marque, LigneDevis, \
    PrestationPneumatique


# Register your models here.


class DevisAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation', 'client')
    list_filter = ('date_creation', 'client',)
    date_hierarchy = 'date_creation'
    ordering = ('id',)
    search_fields = ('client', 'date_creation')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'intitule')
    list_filter = ('intitule',)
    ordering = ('intitule',)
    search_fields = ('intitule',)


admin.site.register(Client, ClientAdmin)
admin.site.register(Marque)
admin.site.register(Categorie)
admin.site.register(Prestation)
admin.site.register(PrestationCoutVariableConcrete)
admin.site.register(PrestationCoutFixe)
admin.site.register(PrestationCoutVariableStandard)
admin.site.register(PieceDetacheeStandard)
admin.site.register(PieceDetacheeAvecPrix)
admin.site.register(PrestationPneumatique)
admin.site.register(LigneDevis)
admin.site.register(Devis, DevisAdmin)
