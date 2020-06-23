# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from django.utils import timezone


class Categorie(models.Model):
    libelle = models.CharField(max_length=50, default="Autres")

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name = "Catégorie"


class PieceDetacheeStandard(models.Model):
    libelle = models.CharField(max_length=50, default="Pièce détachée standard")

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name = "Pièce détachée sans prix"


class PieceDetacheeAvecPrix(PieceDetacheeStandard):
    prix_total = models.FloatField(default=0)

    def __str__(self):
        return "{} - {}€".format(self.libelle, self.prix_total)

    class Meta:
        verbose_name = "Pièce détachée avec prix associé"

def get_autre_categorie():
    return Categorie.objects.get_or_create(libelle="Autres")[0]

class Prestation(models.Model):
    libelle = models.CharField(max_length=50, default="Prestation standard")
    categorie = models.ForeignKey('Categorie', default=get_autre_categorie, on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name = "Prestation standard, sans coût"
        managed = False
        abstract = True

    def __str__(self):
        return self.libelle


class PrestationCoutFixe(Prestation):
    prix_total = models.FloatField(default=0)

    class Meta:
        verbose_name = "Prestation à coût fixe"

    def __str__(self):
        return "{} - {}".format(self.libelle, self.prix_total)


class PrestationCoutVariableStandard(Prestation):
    pieces_detachees = models.ManyToManyField(PieceDetacheeStandard)

    class Meta:
        verbose_name = "Prestation à prix variable, sans prix associés"

    def __str__(self):
        return "{} - {}".format(self.libelle, self.pieces_detachees)


class PrestationCoutVariableConcrete(Prestation):
    pieces_detachees = models.ManyToManyField(PieceDetacheeAvecPrix)

    class Meta:
        verbose_name = "Prestation à prix variable, prix des pièces connus"

    def __str__(self):
        return "{} - {}".format(self.libelle, self.pieces_detachees)


class Devis(models.Model):
    date_creation = models.DateField(default=timezone.now, verbose_name="Date création du devis")
    date_planification = models.DateField(default=timezone.now, verbose_name="Planification prévue pour le devis",
                                          blank=True)
    client = models.ForeignKey('Client', on_delete=models.PROTECT)

    prestations_fixe = models.ManyToManyField(PrestationCoutFixe)
    prestations_variable = models.ManyToManyField(PrestationCoutVariableConcrete)

    reduction = models.IntegerField(default=0)
    oral = models.BooleanField(default=False)

    class Meta:
        verbose_name = "devis"
        ordering = ['id']

    def __str__(self):
        return "n°{} ({}) : {}".format(self.id, self.date_creation, self.client)


class Client(models.Model):
    prenom = models.CharField(max_length=50, blank=True, null=True)
    nom = models.CharField(max_length=50, default="X")
    societe = models.CharField(max_length=100, blank=True, null=True)
    adresse = models.TextField(max_length=200, default="X")
    complement_adresse = models.TextField(max_length=200, blank=True, null=True)
    telephone = PhoneNumberField(null=True, blank=True)

    class Meta:
        verbose_name = "client"
        ordering = ['nom']

    def __str__(self):
        return "{} {} {}".format(self.prenom, self.nom, self.societe or "")
