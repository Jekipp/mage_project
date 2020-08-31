from django.shortcuts import render, redirect
from .models import Game, Player, Card, SUITS, Library
from django.contrib.auth.models import User
from . import game_logic as gl
from django.db.models import Sum


# Create your views here.


def game(request, game_id):
    game = Game.objects.get(id=game_id)
    mine_total = game.mine.all().aggregate(Sum('value'))
    print(mine_total)
    return render(request, 'game.html', {'game': game, 'mine_total': mine_total['value__sum']})
    
def pending_games(request):
    pending = Game.objects.filter(status='P')
    return render(request, 'pending_games.html', {'pending': pending})

def active_games(request):
    active = Game.objects.filter(status='A')
    return render(request, 'active_games.html', {'active': active})

def start_game(request):
    game = Game.objects.create()
    player = Player.objects.create(user=request.user, game=game)
    return redirect('wait_room', game.id)

def wait_room(request, game_id):
    game = Game.objects.get(id=game_id)
    game_players = game.players.all()
    if game_players.count() > 1:
        # add logic handing out cards to players
        game.status = 'A'
        game.save()
        gl.deal_cards(game) 
        return redirect('game', game.id)
    return render(request, 'wait_room.html', {'game': game})

def join_game(request, game_id):
    game = Game.objects.get(id=game_id)
    player, created = Player.objects.get_or_create(user=request.user, game=game)
    return redirect('wait_room', game_id)

def see_game(request, game_id):
    game = Game.objects.get(id=game_id)
    player = game.players.get(user=request.user)
    return redirect('game', game.id)

def card_details(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    player = game.players.get(user=request.user)
    if card.suit =='d':
        return render(request, 'play_diamond.html', {'card': card, 'game': game})
    
    if card.suit =='s':
        return render(request, 'play_spade.html', {'card': card, 'game': game})

    return render(request, 'card_details.html', {'card': card, 'game': game})

def cost(card, player):
    if 14 > card.value > 10:
        card_cost = card.value - 10
    else:
        card_cost = card.value
    if card_cost > player.vault:
        print('cost is greater than player.valut')
        #add message that insufficient funds
        return False
    player.vault -= card_cost
    player.save()
    return True


def card_ability(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    return render(request, 'card_ability.html', {'card': card, 'game': game})

def card_ability2(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    return render(request, 'card_ability2.html', {'card': card, 'game': game})

def ability_target(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    zones = ['court', 'life']
    return render(request, 'ability_target.html', {'card': card, 'game': game, 'zones': zones})



def play_card(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    player = game.players.get(user=request.user)
    if card.suit == 'd':
        print(f'diamond was played: {card.suit} {card.value}')
        return render(request, 'play_diamond.html', {'card': card, 'game': game})

    return render(request, 'play_card.html', {'card': card, 'game': game})


def diamond_mine(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    player = game.players.get(user=request.user)
    # if card.suit =='d':
    player.hand.remove(card)
    game.mine.add(card)
    return redirect('game', game.id)

def diamond_discard(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    player = game.players.get(user=request.user)
    player.hand.remove(card)
    game.discard.add(card)
    # vault += Player.objects.get(vault=vault)
    return redirect('game', game.id)


def diamond_draw(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    player = game.players.get(user=request.user)
    player.hand.remove(card)
    game.discard.add(card)
    new_card = Library.objects.filter(game=game).first().card
    game.library.remove(new_card)
    player.hand.add(new_card)
    return redirect('game', game.id)

def spade_curse(request, game_id, card_id):
    card = Card.objects.get(id=card_id)
    game = Game.objects.get(id=game_id)
    player = game.players.get(user=request.user)

    if cost(card,player):
        print('passed cost')
        player.hand.remove(card)
        game.discard.add(card)
        player2 = game.players.exclude(user=request.user).first()
        player2.health -= card.value
        player2.save()
    return redirect('game', game.id)

            







    # library = Library.objects.get(id=library_id)
    # # card_draw = game.library.get(library_card=card).first()
    # # card_draw = Library.objects.filter(library_card=card)
    # card_draw = Library.objects.index[0]
    # game.library.remove(card_draw)
    # player.hand.add(card_draw)






# def play_from_hand(card_id, game_id):
# 	game = Game.objects.get(id=game_id)
# 	card = Card.objects.get(id=card_id)
# 	player = game.players.get(user=request.user)
# 	if 10 < card.value < 14 :
# 		cost = card.value -10 
# 		if player.vault >= cost:
# 			player.vault -= cost		
# 			player.hand.remove(card)
# 			player.court.add(card)
# 			# success flash message?
# 		else:
# 			#add flash messages that user didnt have enough in his valut to play this card
# 			pass
# 	else:
# 		if card.suit == 'd':
# 			return redirect('play_diamond', card.id)
# 		if card.suit in ['s','h','c']:
# 			if player.vault >= card.value:
# 				player.vault -= cost		
# 				player.hand.remove(card)
# 				player.spellzone.add(card)
# 				# success flash message?
# 			else:
# 				#add flash messages that user didnt have enough in his valut to play this card
# 				pass
# 	return redirect('game')





# def play_card_from_hand(request, game_id, card_id):


# def play_from_hand(card_id, game_id):
# 	game = Game.objects.get(id=game_id)
# 	card = Card.objects.get(id=card_id)
# 	player = game.players.get(user=request.user)
#     if card.suit == 'd':
#     return render(request, 'play_diamond.html', {'card': card, 'game': game})
#     return redirect('card_ability')
    


# 	if 10 < card.value < 14 :
# 		cost = card.value -10 
# 		if player.vault >= cost:
# 			player.vault -= cost		
# 			player.hand.remove(card)
# 			player.court.add(card)
# 			# success flash message?
# 		else:
# 			#add flash messages that user didnt have enough in his valut to play this card
# 			pass
# 	else:
# 		if card.suit == 'd':
# 			return redirect('play_diamond', card.id)
# 		if card.suit in ['s','h','c']:
# 			if player.vault >= card.value:
# 				player.vault -= cost		
# 				player.hand.remove(card)
# 				player.spellzone.add(card)
# 				# success flash message?
# 			else:
# 				#add flash messages that user didnt have enough in his valut to play this card
# 				pass
# 	return redirect('game')

# def play_diamond(request, card_id, game_id):
#     game = Game.objects.get(id=game_id)
#     card = Card.objects.get(id=card_id)
#     player = game.players.get(user=request.user)
#     return render(request, 'play_diamond.html', {'card': card, 'game': game})





