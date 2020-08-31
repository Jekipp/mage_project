from django.db import models
from django.contrib.auth.models import User

# Create your models here.

SUITS = [
('s', 'Spade'),
('c', 'Club'),
('d', 'Diamond'),
('h', 'Heart')
]

class Game(models.Model):
	CHOICES = [
		('P', 'Pending'),
		('A', 'Active'),
		('F', 'Finished'),
	]
	PHASES = [
		('I', 'Idle'),
		('R', 'Reset'),
		('M', 'Main'),
	]
	library = models.ManyToManyField('Card', through='Library', related_name='library')
	mine = models.ManyToManyField('Card', related_name='mine')
	discard = models.ManyToManyField('Card', related_name='discard')
	status = models.CharField(max_length=8, choices=CHOICES, default='P')
	phase = models.CharField(max_length=8, choices=PHASES, default='I')
	# duelzone = models.ManyToManyField('Card', through='Duelzone')
	spellzone = models.ManyToManyField('Card', through='Spellzone', blank=True)


class Library(models.Model):
	card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='library_card')
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='library_game')
	index = models.IntegerField()

	class Meta:
		ordering = ['index']


class Spellzone(models.Model):
	card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='spell_card')
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='spell_game')
	player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='spell_player')


class Duelzone(models.Model):
	card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='duel_card')
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='duel_game')
	player = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='duel_player')


class Player(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='player_user')
	hand = models.ManyToManyField('Card', related_name='player_hand', blank=True)
	health = models.IntegerField(default=30)
	vault = models.IntegerField(default=0)
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
	court = models.ManyToManyField('Card', related_name='player_court')


class Card(models.Model):

	suit = models.CharField(choices=SUITS, max_length=7)
	value = models.IntegerField()
	


# class Card(models.Model):
# 	suits = [
# 				('s', 'Spade'),
# 				('c', 'Club'),
# 				('d', 'Diamond'),
# 				('h', 'Heart'),
# 				('r', 'Royal'),
# 				('j', 'Joker'),
# 			]
# 	suit = models.CharField(choices=suits, max_length=7)
# 	value = models.IntegerField()

# 	def make_cards(self, value, suit):
# 		for s in suits:
# 			for v in range(1,10):
# 				spade_cards = Card.objects.get_or_create(value=v, suit=suit[0])
# 		for c in club:
# 			for v in range(1,10):
# 				spade_cards = Card.objects.get_or_create(value=v, suit=suit[0])
# 		for h in heart:
# 			for v in range(1,10):
# 				spade_cards = Card.objects.get_or_create(value=v, suit=suit[0])
# 		for d in daimond:
# 			for v in range(1,10):
# 				spade_cards = Card.objects.get_or_create(value=v, suit=suit[0])
# 		for r in royal:
# 			for v in range(1,3):
# 				spade_cards = Card.objects.get_or_create(value=v, suit=suit[0])
# 		for j in joker:
# 			for v in range(1,2):
# 				spade_cards = Card.objects.get_or_create(value=v, suit=suit[0])
		
# 		def deal_cards(self, game):
# 			temp_library = Card.objects.all()
# 			random.shuffle(list(temp_library))
# 	# add shuffled game deck to the game
# 			for card in temp_library:
# 			game.library.add(card)
# 	# deal out 7 cards per player
# 			for num in range(7):
# 				for player in game.players.all():
# 					card = game.library.first()
# 					game.library.remove(card)
# 					player.hand.add(card)

