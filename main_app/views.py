import random
import requests
from django import forms
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from .models import Pokemon, Item
from .forms import PokemonNicknameForm, FeedingForm, ItemForm

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
            poke_type = data['types'][0]['type']['name']
            abilities = ', '.join([ability['ability']['name'] for ability in data['abilities']])
            image_url = data['sprites']['other']['official-artwork']['front_default']
            return {
                'name': name,
                'poke_id': poke_id,
                'xp': xp,
                'type': poke_type,
                'abilities': abilities,
                'image_url': image_url
            }
        
        else:
            return None

    random_pokemon = fetch_random_pokemon()
    return render(request, 'pokemon/index.html', {'pokemon': random_pokemon})

def poke_detail(request, poke_id):
    pokemon = Pokemon.objects.get(poke_id=poke_id)
    # Only show items that the pokemon doesn't have.
    items_pokemon_doesnt_have = Item.objects.exclude(id__in=pokemon.items.all().values_list('id'))
    feeding_form = FeedingForm()

    return render(request, 'pokemon/detail.html', {
        'pokemon': pokemon,
        'feedings': pokemon.feedings.all(),
        'feeding_form': feeding_form,
        'items': items_pokemon_doesnt_have,
    })

def catch_pokemon(request, poke_id):
    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{poke_id}/')
    
    if response.status_code == 200:
        data = response.json()
        name = data['name'].capitalize()
        poke_id = data['id']
        xp = data['base_experience']
        poke_type = data['types'][0]['type']['name']
        abilities = ', '.join([ability['ability']['name'] for ability in data['abilities']])
        image_url = data['sprites']['other']['official-artwork']['front_default']
        
        pokemon = Pokemon(
            name=name,
            poke_id=poke_id,
            xp=xp,
            type=poke_type,
            abilities=abilities,
            image_url=image_url
        )
        
        pokemon.save()

        return redirect('show-pokemon')
    else:
        return HttpResponse('Error fetching data from the Pokémon API')
    
def show_pokemon(request):
    pokemon = Pokemon.objects.all()
    return render(request, 'pokemon/show.html', {'pokemon': pokemon})

class PokemonDelete(DeleteView):
    model = Pokemon
    success_url = reverse_lazy('show-pokemon')

def update_nickname(request, poke_id):
    try:
        pokemon = Pokemon.objects.get(poke_id=poke_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound("Pokemon not found")

    if request.method == 'POST':
        form = PokemonNicknameForm(request.POST, instance=pokemon)
        if form.is_valid():
            form.save()
            return redirect('show-pokemon')
    else:
        form = PokemonNicknameForm(instance=pokemon)

    return render(request, 'pokemon/update_nickname.html', {'form': form, 'pokemon': pokemon})

def add_feeding(request, poke_id):
    form = FeedingForm(request.POST)

    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.pokemon_id = poke_id
        new_feeding.save()
    return redirect('poke-detail', poke_id=poke_id)

class ItemCreate(CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item-index')

    def form_valid(self, form):
        item_name = form.cleaned_data['name']
        response = requests.get(f'https://pokeapi.co/api/v2/item/{item_name}/')

        if response.status_code == 200:
            data = response.json()
            form.instance.cost = data.get('cost', 0)
            form.instance.effect = data.get('effect_entries')[0].get('effect')
            form.instance.flavor_text = data.get('flavor_text_entries')[0].get('text')
            form.instance.sprite_url = data.get('sprites').get('default')

        form.save()
        return redirect(self.success_url)

class ItemList(ListView):
    model = Item
    template_name = 'items/item_index.html'
    context_object_name = 'items'

class ItemDetail(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'

class ItemUpdate(UpdateView):
    model = Item
    fields = ['name', 'cost', 'effect', 'flavor_text', 'note']
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('item-index')

class ItemDelete(DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('item-index')

def give_item(request, pokemon_id, item_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    pokemon.items.add(item_id)
    return redirect('poke-detail', poke_id = pokemon.poke_id)

def remove_item(request, pokemon_id, item_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    item = Item.objects.get(id=item_id)
    pokemon.items.remove(item)
    return redirect('poke-detail', poke_id=pokemon.poke_id)

