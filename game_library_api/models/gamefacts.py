from django.db import models
from .game import Game


class Gamefacts(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE, related_name="facts")
    fact = models.CharField(max_length=150)
