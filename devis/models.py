# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone


class Prestation(models.Model):
    prix = models.FloatField(default=0)
    titre = models.CharField(max_length=50, default="Prestation X")

    class Meta:
        verbose_name = "prestation"
        ordering = ['titre']

    def __str__(self):
        return "{} {:,.2f}€".format(self.titre, self.prix)


class Devis(models.Model):
    date_creation = models.DateField(default=timezone.now, verbose_name="Date création du devis")
    date_planification = models.DateField(default=timezone.now, verbose_name="Planification prévue pour le devis",
                                          null=True)
    client = models.ForeignKey('Client', on_delete=models.PROTECT)
    prestations = models.Field('Prestation', on_delete=models.SET_NULL, null=True)
    reduction = models.IntegerField(default=0, max_length=2)
    oral = models.BooleanField(default=False)

    class Meta:
        verbose_name = "devis"
        ordering = ['date_creation']

    def __str__(self):
        return "n°{} ({}) : \n{}".format(self.id, self.date_creation, self.client)


class Client(models.Model):
    prenom = models.CharField(max_length=50, null=True)
    nom = models.CharField(max_length=50, null=True)
    societe = models.CharField(max_length=100, null=True)
    adresse = models.TextField(max_length=200)
    complement_adresse = models.TextField(max_length=200, null=True)

    class Meta:
        verbose_name = "client"
        ordering = ['nom']

    def __str__(self):
        return "{} {} ({}) : {}".format(self.prenom, self.nom, self.societe, self.adresse)
