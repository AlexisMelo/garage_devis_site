from django import forms
from django.forms import ModelMultipleChoiceField

from prestations.models import PrestationCoutFixe, PrestationCoutVariableStandard


class CreatePrestationCoutFixeForm(forms.ModelForm):
    class Meta:
        model = PrestationCoutFixe
        fields = ('libelle', 'categorie', 'prix')
        widgets = {
            'prix': forms.NumberInput(attrs={'min': '0', 'step': '0.01'})
        }


class CreatePrestationCoutVariableForm(forms.ModelForm):

    pieces_detachees = forms.MultipleChoiceField

    class Meta:
        model = PrestationCoutVariableStandard
        fields = ('libelle', 'categorie', 'pieces_detachees')
