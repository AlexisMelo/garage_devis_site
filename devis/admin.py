# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Devis, Client, Prestation, PrestationCoutVariableConcrete, PrestationCoutFixe, \
    PrestationCoutVariableStandard, PieceDetacheeStandard, PieceDetacheeAvecPrix, Categorie


# Register your models here.


class DevisAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation', 'client', 'oral')
    list_filter = ('date_creation', 'client', 'oral', )
    date_hierarchy = 'date_creation'
    ordering = ('id',)
    search_fields = ('client', 'date_creation')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'prenom', 'nom', 'societe')
    list_filter = ('prenom', 'nom', 'societe',)
    ordering = ('nom', 'prenom',)
    search_fields = ('prenom', 'nom', 'societe')


admin.site.register(Devis, DevisAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Categorie)
admin.site.register(PrestationCoutVariableConcrete)
admin.site.register(PrestationCoutFixe)
admin.site.register(PrestationCoutVariableStandard)
admin.site.register(PieceDetacheeStandard)
admin.site.register(PieceDetacheeAvecPrix)
