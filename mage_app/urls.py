from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
        path('game/<int:game_id>/', views.game, name='game'),
        path('pending_games', views.pending_games, name='pending_games'),
        path('active_games', views.active_games, name='active_games'),
        path('start_game/', views.start_game, name='start_game'),
        path('wait_room/<int:game_id>/', views.wait_room, name='wait_room'),
        path('join_game/<int:game_id>/', views.join_game, name='join_game'),
        
        path('card_details/<int:game_id>/<int:card_id>', views.card_details, name='card_details'),
        # path('play_card_from_hand/<int:game_id>/<int:card_id>', views.card_details, name='play_card_from_hand'),
        
        path('play_card/<int:game_id>/<int:card_id>', views.play_card, name='play_card'),

        path('card_ability/<int:game_id>/<int:card_id>', views.card_ability, name='card_ability'),
        path('card_ability2/<int:game_id>/<int:card_id>', views.card_ability2, name='card_ability2'),
        path('ability_target/<int:game_id>/<int:card_id>', views.ability_target, name='ability_target'),
        
        path('play_diamond/<int:game_id>/<int:card_id>', views.diamond_mine, name='diamond_mine'),
        path('diamond_discard/<int:game_id>/<int:card_id>', views.diamond_discard, name='diamond_discard'),
        path('diamond_draw/<int:game_id>/<int:card_id>', views.diamond_draw, name='diamond_draw'),

        path('play_spade/<int:game_id>/<int:card_id>', views.spade_curse, name='spade_curse'),







]

