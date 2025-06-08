from django.db import models

class Adventurer(models.Model):
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50)
    character_class = models.CharField(max_length=50)
    level = models.PositiveIntegerField(default=1)

    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    intelligence = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)

    background = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} the {self.race} {self.character_class} (Lvl {self.level})"