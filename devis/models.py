# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse
from django.utils.datetime_safe import date
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from django.utils import timezone

from prestations.models import Prestation


class LigneDevis(models.Model):
    prestation = models.ForeignKey(Prestation, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Ligne d'un devis"

    @property
    def prix_total(self):
        return self.quantite * self.prestation.prix_total


class Client(models.Model):
    intitule = models.CharField(max_length=100)
    adresse = models.TextField(max_length=200, blank=True, null=True)
    complement_adresse = models.TextField(max_length=200, blank=True, null=True)
    telephone = PhoneNumberField(null=True, blank=True)
    date_ajout = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Client"
        ordering = ['intitule']

    def __str__(self):
        return self.intitule

    def get_absolute_url(self):
        return reverse('client_detail', args=[str(self.id)])

    @property
    def devis(self):
        return Devis.objects.filter(client=self)

    def temps_client_formatte(self):
        nbJours = (date.today() - self.date_ajout).days

        annees = int(nbJours / 365)
        semaines = int((nbJours % 365) / 7)
        jours = (nbJours % 365) % 7

        retour = []

        retour.append(pluriel(annees, "année"))
        retour.append(pluriel(semaines, "semaine"))
        retour.append(pluriel(jours, "jour"))

        return ", ".join(filter(None,retour))

class Devis(models.Model):
    date_creation = models.DateField(default=timezone.now, verbose_name="Date création du devis")
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    lignes = models.ManyToManyField(LigneDevis)

    reduction = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Devis"
        ordering = ['id']

    def __str__(self):
        return "n°{} ({}) : {}".format(self.id, self.date_creation, self.client)

    @property
    def prix_total(self):
        return sum([ligne.prix_total for ligne in self.lignes.all()])

    @property
    def prest_str(self):
        str = " + ".join([ligne.prestation.get_libelle() for ligne in self.lignes.all()])
        return str

def pluriel(quantite, mot):
    if quantite != 0:

        if quantite == 1:
            return "1 {}".format(mot)

        return "{} {}s".format(quantite, mot)
    return None
