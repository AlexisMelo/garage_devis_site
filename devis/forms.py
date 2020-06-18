from django import forms
from .models import Devis

class PrestationAjoutForm(forms.Form):
    prix = forms.FloatField()
    titre = forms.CharField(max_length=50, label="Titre de la préstation")

class DevisAjoutForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = '__all__'

class DevisModifForm(forms.ModelForm):
    class Meta:
        model = Devis
        fields = '__all__'