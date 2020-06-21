from django.contrib.auth.models import User
from django.db import models


class Garage(models.Model):
    libelle = models.CharField(max_length=50)
    adresse = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "garage"
        ordering = ['libelle']

    def __str__(self):
        return self.libelle


class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    garage = models.ForeignKey('Garage', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "employe"
        ordering = ['garage']

    def __str__(self):
        return "{} {} de {}".format(self.user.nom, self.user.prenom, self.garage)
