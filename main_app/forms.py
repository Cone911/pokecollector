from django import forms
from .models import Pokemon

class PokemonNicknameForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['nickname']