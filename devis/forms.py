from django import forms
from django.forms import DateInput, CharField

from .models import Devis, Client


class ClientAjoutForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
