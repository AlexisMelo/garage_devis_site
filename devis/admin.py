# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Devis, Client, LigneDevis

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
admin.site.register(LigneDevis)
admin.site.register(Devis, DevisAdmin)
