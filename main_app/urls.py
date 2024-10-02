from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pokemon/', views.index, name='pokemon-index'),
    path('pokemon/<int:poke_id>/', views.poke_detail, name='poke-detail'),
    path('pokemon/add/<int:poke_id>', views.AddPokemonView.as_view(), name='add-pokemon')
]
