from django.db import models
from .gamer import Gamer


class Friendlist(models.Model):
    gamer = models.ForeignKey("game_library_api.Gamer",
                              on_delete=models.CASCADE, related_name="follower")
    friend = models.ForeignKey(
        "game_library_api.Gamer", on_delete=models.CASCADE, related_name="friend")

    date = models.DateTimeField(auto_now_add=True)
