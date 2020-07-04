# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from django.utils import timezone
from polymorphic.models import PolymorphicModel


class Categorie(models.Model):
    libelle = models.CharField(max_length=50, default="Autres")
    icone = models.CharField(max_length=50, default="miscellaneous_services", blank=True)

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
    prix = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return "{} - {}€".format(self.libelle, self.prix)

    class Meta:
        verbose_name = "Pièce détachée avec prix associé"

    @property
    def prix_total(self):
        return self.prix

def get_autre_categorie():
    return Categorie.objects.get_or_create(libelle="Autres")[0]


class Prestation(PolymorphicModel):
    libelle = models.CharField(max_length=50, default="Prestation standard")
    categorie = models.ForeignKey('Categorie', default=get_autre_categorie, on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name = "Prestation standard, sans coût"

    def __str__(self):
        return self.libelle

    @property
    def prix_total(self):
        return 0


class PrestationCoutFixe(Prestation):
    prix = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Prestation à coût fixe"

    def __str__(self):
        return "{} - {}".format(self.libelle, self.prix)

    @property
    def prix_total(self):
        return self.prix


class PrestationCoutVariableStandard(Prestation):
    pieces_detachees = models.ManyToManyField(PieceDetacheeStandard)

    class Meta:
        verbose_name = "Prestation à prix variable, sans prix associés"

    def __str__(self):
        return "{} - {}".format(self.libelle, self.pieces_detachees)

    @property
    def prix_total(self):
        return 0


class PrestationCoutVariableConcrete(Prestation):
    pieces_detachees = models.ManyToManyField(PieceDetacheeAvecPrix)

    class Meta:
        verbose_name = "Prestation à prix variable, prix des pièces connus"

    def __str__(self):
        return "{} - {}".format(self.libelle, self.pieces_detachees)

    @property
    def prix_total(self):
        return sum([piece.prix for piece in self.pieces_detachees.all()])


class LigneDevis(models.Model):
    prestation = models.ForeignKey('Prestation', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Ligne d'un devis"

    @property
    def prix_total(self):
        return self.quantite * self.prestation.prix_total


class Devis(models.Model):
    date_creation = models.DateField(default=timezone.now, verbose_name="Date création du devis")
    date_planification = models.DateField(default=timezone.now, verbose_name="Planification prévue pour le devis")
    client = models.ForeignKey('Client', on_delete=models.PROTECT)

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


class Marque(models.Model):
    libelle = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Marque"


class PrestationPneumatique(Prestation):
    prixAchat = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    dimensions = models.PositiveIntegerField()
    marque = models.ForeignKey('Marque', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Prestation concernant les pneus"

    @property
    def prix_total(self):
        TVA = Decimal(1.2)
        marge = Decimal(11.5)

        prixttc = self.prixAchat

        if self.dimensions < 19:
            prixttc += self.dimensions - 3
        else:
            prixttc += self.dimensions

        prixttc *= TVA
        prixttc += marge

        return round(prixttc, 2)

class PrestationMainOeuvre(Prestation):
    tauxHoraire = models.DecimalField(max_digits=7, decimal_places=2, default=55)

    class Meta:
        verbose_name = "Prestation representant 1 heure de main d'oeuvre"

    @property
    def prix_total(self):
        return self.tauxHoraire