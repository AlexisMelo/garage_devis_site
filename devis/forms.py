from django import forms
from .models import Devis, Prestation


class PrestationAjoutForm(forms.ModelForm):
    class Meta:
        model = Prestation
        fields = '__all__'

class DevisAjoutForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = '__all__'

class DevisModifForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = '__all__'