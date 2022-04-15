from django.db import models
from .gamer import Gamer
from .category import Category


class Game(models.Model):
    gamer = models.ForeignKey(
        Gamer, on_delete=models.CASCADE, related_name="my_games")
    title = models.CharField(max_length=20)

    description = models.CharField(max_length=150)

    date = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="assigned_game")
