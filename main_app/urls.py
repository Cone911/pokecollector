from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pokemon/', views.index, name='pokemon-index'),
    path('pokemon/<int:poke_id>/', views.poke_detail, name='poke-detail'),
    path('pokemon/<int:poke_id>/catch', views.catch_pokemon, name='catch-pokemon'),
    path('pokemon/show', views.show_pokemon, name='show-pokemon'),
    path('pokemon/<int:pk>/delete/', views.PokemonDelete.as_view(), name='pokemon-delete'),
    path('pokemon/<int:poke_id>/update-nickname/', views.update_nickname, name='update-nickname'),
    path('pokemon/<int:poke_id>/add-feeding/', views.add_feeding, name='add-feeding'),
]
