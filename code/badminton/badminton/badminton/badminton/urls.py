from django.contrib import admin
from django.urls import path
from .views import (
    index, add_player, view_players, start_tournament, next_round, reset_tournament, delete_player,
    start_double_elimination_tournament, double_next_round,edit_player,
    turn_tournament,generate_all_matches,turn_next_round,view_matches,calculate_champions,turn_reset_tournament
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('add-player/', add_player, name='add_player'),
    path('edit_player/<int:player_id>/', edit_player, name='edit_player'),
    path('view-players/', view_players, name='view_players'),
    path('start-tournament/', start_tournament, name='start_tournament'),
    path('next-round/', next_round, name='next_round'),
    path('double_next-round/', double_next_round, name='double_next-round'),
    path('reset-tournament/', reset_tournament, name='reset_tournament'),
    path('delete-player/<int:player_id>/', delete_player, name='delete_player'),
    path('start_double_elimination_tournament/', start_double_elimination_tournament, name='start_double_elimination_tournament'),
    path('turn_tournament/',turn_tournament, name='turn_tournament'),
    path('generate_all_matches/', generate_all_matches, name='generate_all_matches'),
    path('turn_next_round/', turn_next_round, name='turn_next_round'),
    path('view_matches/', view_matches, name='view_matches'),
    path('calculate_champions/', calculate_champions, name='calculate_champions'),
    path('turn_reset_tournament/', turn_reset_tournament, name='turn_reset_tournament'),
]
