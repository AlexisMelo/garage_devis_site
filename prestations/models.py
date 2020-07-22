from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from polymorphic.models import PolymorphicModel

class Categorie(models.Model):
    libelle = models.CharField(max_length=50, default="Autres")
    icone = models.CharField(max_length=50, default="miscellaneous_services", blank=True)

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name = "Catégorie"
        db_table = "prestations_categorie"


class PieceDetacheeStandard(models.Model):
    libelle = models.CharField(max_length=50, default="Pièce détachée standard")

    def __str__(self):
        return self.libelle

    class Meta:
        verbose_name = "Pièce détachée standard"
        db_table = "prestations_piecedetacheestandard"


class PieceDetacheeAvecPrix(PieceDetacheeStandard):
    prix = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    def __str__(self):
        return "{} - {}€".format(self.libelle, self.prix)

    class Meta:
        verbose_name = "Pièce détachée tarifée"
        db_table = "prestations_piecedetacheeavecprix"

    @property
    def prix_total(self):
        return self.prix


def get_autre_categorie():
    return Categorie.objects.get_or_create(libelle="Autres")[0]


class Prestation(PolymorphicModel):
    libelle = models.CharField(max_length=50, default="Prestation standard")
    categorie = models.ForeignKey(Categorie, default=get_autre_categorie, on_delete=models.SET_DEFAULT)

    class Meta:
        verbose_name = "Prestation standard, sans coût"
        db_table = "prestations_prestation"

    def __str__(self):
        return self.get_libelle()

    @property
    def prix_total(self):
        return 0

    def get_libelle(self):
        return self.libelle


class PrestationCoutFixe(Prestation):
    prix = models.DecimalField(max_digits=7, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0.01'))])

    class Meta:
        verbose_name = "Prestation à coût fixe"
        db_table = "prestations_prestationcoutfixe"

    def __str__(self):
        return "{} - {}".format(self.get_libelle(), self.prix)

    @property
    def prix_total(self):
        return self.prix


class PrestationCoutVariableStandard(Prestation):
    pieces_detachees = models.ManyToManyField(PieceDetacheeStandard)

    class Meta:
        verbose_name = "Prestation à prix variable"
        db_table = "prestations_prestationcoutvariablestandard"

    def __str__(self):
        return "{} - {}".format(self.get_libelle(), self.pieces_detachees)

    @property
    def prix_total(self):
        return 0

    @property
    def champs_str(self):
        return ", ".join([p.libelle for p in self.pieces_detachees.all()])


class PrestationCoutVariableConcrete(Prestation):
    pieces_detachees = models.ManyToManyField(PieceDetacheeAvecPrix)

    class Meta:
        verbose_name = "Prestation à prix variable tarifée"
        db_table = "prestations_prestationcoutvariableconcrete"

    def __str__(self):
        return "{} - {}".format(self.get_libelle(), self.pieces_detachees)

    @property
    def prix_total(self):
        return sum([piece.prix for piece in self.pieces_detachees.all()])

    @property
    def champs_str(self):
        return ", ".join([p.libelle for p in self.pieces_detachees.all()])

class Marque(models.Model):
    libelle = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Marque"
        db_table = "prestations_marque"


class PrestationPneumatique(Prestation):
    prixAchat = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    dimensions = models.PositiveIntegerField()
    marque = models.ForeignKey(Marque, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Prestation concernant les pneus"
        db_table = "prestations_prestationpneumatique"

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

    def get_libelle(self):
        if self.marque:
            return '{} {}"'.format(self.marque.libelle, self.dimensions)
        else:
            return 'pneu {}"'.format(self.dimensions)

class PrestationMainOeuvre(Prestation):
    tauxHoraire = models.DecimalField(max_digits=7, decimal_places=2, default=55)

    class Meta:
        verbose_name = "Prestation representant 1 heure de main d'oeuvre"
        db_table = "prestations_prestationmainoeuvre"

    @property
    def prix_total(self):
        return self.tauxHoraire

class PrestationNouvelle(Prestation):
    prix = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Prestation répondant à un besoin ponctuel"
        db_table = "prestations_prestationnouvelle"

    @property
    def prix_total(self):
        return self.prix