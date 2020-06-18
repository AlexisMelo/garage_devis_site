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
                                          blank=True)
    client = models.ForeignKey('Client', on_delete=models.PROTECT)
    prestations = models.ManyToManyField(Prestation)
    reduction = models.IntegerField(default=0)
    oral = models.BooleanField(default=False)

    class Meta:
        verbose_name = "devis"
        ordering = ['date_creation']

    def __str__(self):
        return "n°{} ({}) : {}\nPrestations : {}".format(self.id, self.date_creation, self.client, self.prestations.all())


class Client(models.Model):
    prenom = models.CharField(max_length=50, blank=True)
    nom = models.CharField(max_length=50)
    societe = models.CharField(max_length=100, blank=True)
    adresse = models.TextField(max_length=200)
    complement_adresse = models.TextField(max_length=200, blank=True)

    class Meta:
        verbose_name = "client"
        ordering = ['nom']

    def __str__(self):
        return "{} {} ({}) : {}".format(self.prenom, self.nom, self.societe, self.adresse)
