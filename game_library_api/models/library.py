from django.db import models
from .gamer import Gamer
from .game import Game


class Library(models.Model):
    gamer = models.ForeignKey(
        Gamer, on_delete=models.CASCADE, related_name="library_item")
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="game_in_library")
    isFavorite = models.BooleanField(null=False)
