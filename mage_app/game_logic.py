import random
from .models import Card, Library
# def deal_cards(game):
# 	temp_library = Card.objects.all()
# 	random.shuffle(list(temp_library))
# 	# add shuffled game deck to the game
# 	for card in temp_library:
# 		game.library.add(card)
# 	# deal out 7 cards per player
# 	for num in range(7):
# 		for player in game.players.all():
# 			card = game.library.first()
# 			game.library.remove(card)
# 			player.hand.add(card)


def deal_cards(game):
	temp_library = [card for card in Card.objects.all()]
	random.shuffle(temp_library)
	# add shuffled game deck to the game
	for index, card in enumerate(temp_library):
		Library.objects.create(game=game, card=card, index=index)
	# deal out 7 cards per player
	for num in range(7):
		for player in game.players.all():
			card = Library.objects.filter(game=game).first().card
			game.library.remove(card)
			player.hand.add(card)



