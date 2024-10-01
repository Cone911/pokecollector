import random
import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import Pokemon

class Pokemon:
    def __init__(self, name, poke_id, xp, type, abilities, image_url):
        self.name = name
        self.poke_id = poke_id
        self.xp = xp
        self.type = type
        self.abilities = abilities
        self.image_url = image_url

def home(request):
  return render(request, 'pokemon/home.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    def fetch_random_pokemon():
        random_index = random.randint(1, 150)
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{random_index}/')
        if response.status_code == 200:
            data = response.json()
            name = data['name'].capitalize()
            poke_id = data['id']
            xp = data['base_experience']
            type = data['types'][0]['type']['name']
            abilities = ', '.join([ability['ability']['name'] for ability in data['abilities']])
            image_url = data['sprites']['other']['official-artwork']['front_default']
            return Pokemon(name, poke_id, xp, type, abilities, image_url)
        else:
            return None

    random_pokemon = fetch_random_pokemon()
    return render(request, 'pokemon/index.html', {'pokemon': random_pokemon})

def poke_detail(request, poke_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_id}/')
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        poke_id = data['id']
        xp = data['base_experience']
        type = data['types'][0]['type']['name']
        abilities = ', '.join([ability['ability']['name'] for ability in data['abilities']])
        moves = ', '.join([move['move']['name'] for move in data['moves']])
        image_url = data['sprites']['other']['official-artwork']['front_default']
        return render(request, 'pokemon/detail.html', {'pokemon': Pokemon(name, poke_id, xp, type, abilities, image_url), 'moves': moves})
    else:
        return HttpResponse('Error fetching data')
    
