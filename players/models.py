from django.db import models
from django.conf import settings

class Character(models.Model):
    CLASS_CHOICES = [
        ('barbarian', 'Barbarian'),
        ('bard', 'Bard'),
        ('cleric', 'Cleric'),
        ('druid', 'Druid'),
        ('fighter', 'Fighter'),
        ('monk', 'Monk'),
        ('paladin', 'Paladin'),
        ('ranger', 'Ranger'),
        ('rogue', 'Rogue'),
        ('sorcerer', 'Sorcerer'),
        ('warlock', 'Warlock'),
        ('wizard', 'Wizard'),
    ]

    RACE_CHOICES = [
        ('dragonborn', 'Dragonborn'),
        ('dwarf', 'Dwarf'),
        ('elf', 'Elf'),
        ('gnome', 'Gnome'),
        ('half_elf', 'Half-Elf'),
        ('halfling', 'Halfling'),
        ('half_orc', 'Half-Orc'),
        ('human', 'Human'),
        ('tiefling', 'Tiefling'),
        ('giff', 'Giff'),
    ]

    name = models.CharField(max_length=100)
    level = models.PositiveIntegerField()
    character_class = models.CharField(max_length=20, choices=CLASS_CHOICES)
    race = models.CharField(max_length=20, choices=RACE_CHOICES)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='characters'   # umożliwia user.characters.all()
    )

    def __str__(self):
        return f"{self.name} the {self.race} {self.character_class.capitalize()} (Level {self.level})"
