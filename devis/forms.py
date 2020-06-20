from django import forms
from django.forms import DateField, DateInput, TextInput

from .models import Devis, Prestation


class PrestationAjoutForm(forms.ModelForm):
    class Meta:
        model = Prestation
        fields = '__all__'

class DevisAjoutForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['date_planification','client','prestations','reduction']
        widgets = {
            'date_planification': DateInput(attrs={'format' : 'dd-mm-yyyy','class': 'datepicker'})
        }

class DevisModifForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = ['date_planification','client','prestations','reduction']
        widgets = {
            'date_planification': DateInput(attrs={'format': 'dd-mm-yyyy', 'class': 'datepicker'})
        }