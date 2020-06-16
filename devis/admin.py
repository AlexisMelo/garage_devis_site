# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Devis, Client, Prestation


# Register your models here.


class DevisAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_creation', 'client', 'oral')
    list_filter = ('date_creation', 'client', 'oral', 'prestations',)
    date_hierarchy = 'date_creation'
    ordering = ('date_creation',)
    search_fields = ('client', 'date_creation')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'prenom', 'nom', 'societe')
    list_filter = ('prenom', 'nom', 'societe',)
    ordering = ('nom', 'prenom',)
    search_fields = ('prenom', 'nom', 'societe')


class PrestationAdmin(admin.ModelAdmin):
    list_display = ('id', 'titre', 'prix')
    list_filter = ('titre',)
    ordering = ('titre',)
    search_fields = ('titre',)


admin.site.register(Devis, DevisAdmin)
admin.site.register(Prestation, PrestationAdmin)
admin.site.register(Client, ClientAdmin)
