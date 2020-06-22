from django import forms
from django.forms import DateInput

from .models import Devis


class DevisAjoutForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['date_planification', 'client', 'prestations_fixe', 'prestations_variable', 'reduction']
        widgets = {
            'date_planification': DateInput(attrs={'format': 'dd-mm-yyyy', 'class': 'datepicker'})
        }


class DevisModifForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['date_planification', 'client', 'prestations_fixe','prestations_variable', 'reduction']
        widgets = {
            'date_planification': DateInput(attrs={'format': 'dd-mm-yyyy', 'class': 'datepicker'})
        }