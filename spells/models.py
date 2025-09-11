from django.db import models


class Spell(models.Model):
    # Use API index as primary key (np acid-arrow)
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200)
    level = models.IntegerField(default=0)
    ritual = models.BooleanField(default=False)
    concentration = models.BooleanField(default=False)
    components = models.JSONField(default=list)
    casting_time = models.CharField(max_length=200)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (lvl {self.level})"
