from django import forms

from prestations.models import PrestationCoutFixe


class CreatePrestationCoutFixeForm(forms.ModelForm):

    class Meta:
        model = PrestationCoutFixe
        fields = ('libelle', 'categorie', 'prix')
        widgets = {
            'prix': forms.NumberInput(attrs={'min':'0','step':'0.01'})
        }