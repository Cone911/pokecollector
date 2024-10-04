from django import forms
from .models import Pokemon, Feeding

class PokemonNicknameForm(forms.ModelForm):
    class Meta:
        model = Pokemon
        fields = ['nickname']

class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ['date', 'meal']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={
                    'placeholder': 'Select a date',
                    'type': 'date'
                }
            ),
        }