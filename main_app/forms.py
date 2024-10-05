from django import forms
from .models import Pokemon, Feeding, Item
import requests

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

class ItemForm(forms.ModelForm):
    name = forms.ChoiceField(choices=[])

    class Meta:
        model = Item
        fields = ['name', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].choices = self.fetch_item_choices()

    def fetch_item_choices(self):
        response = requests.get('https://pokeapi.co/api/v2/item?limit=20')
        data = response.json()
        choices = []
        for item in data['results']:
            choices.append((item['name'], item['name'].capitalize()))
        return choices