# character_structure/models.py
from django.db import models
from spells.models import Spell

class Subclass(models.Model):
    id = models.CharField(primary_key=True, max_length=100)  # np. cleric_life_domain
    name = models.CharField(max_length=200)
    spells = models.ManyToManyField(Spell, blank=True)

    def __str__(self):
        return self.name

class SubclassSpell(models.Model):
    subclass = models.ForeignKey(Subclass, on_delete=models.CASCADE, related_name="subclass_spells")
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    level_granted = models.IntegerField()  # level at which subclass gains this spell
    always_prepared = models.BooleanField(default=True)  # PHB subclass spells are usually always prepared

    class Meta:
        unique_together = ("subclass", "spell")

    def __str__(self):
        return f"{self.subclass.name} → {self.spell.name} (lvl {self.level_granted})"


class Class(models.Model):
    id = models.CharField(primary_key=True, max_length=100)  # np. cleric, wizard
    name = models.CharField(max_length=200)
    possible_spells = models.ManyToManyField(Spell, blank=True)
    subclasses = models.ManyToManyField(Subclass, blank=True)

    def __str__(self):
        return self.name
