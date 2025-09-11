from django.db import models
from django.conf import settings
import requests

# PHB classes and subclasses map
CLASS_SUBCLASS_MAP = {
    "barbarian": {
        "name": "Barbarian",
        "subclasses": {
            "barbarian_berserker": "Path of the Berserker",
            "barbarian_totem_warrior": "Path of the Totem Warrior",
        },
    },
    "bard": {
        "name": "Bard",
        "subclasses": {
            "bard_lore": "College of Lore",
            "bard_valor": "College of Valor",
        },
    },
    "cleric": {
        "name": "Cleric",
        "subclasses": {
            "cleric_knowledge_domain": "Knowledge Domain",
            "cleric_life_domain": "Life Domain",
            "cleric_light_domain": "Light Domain",
            "cleric_nature_domain": "Nature Domain",
            "cleric_tempest_domain": "Tempest Domain",
            "cleric_trickery_domain": "Trickery Domain",
            "cleric_war_domain": "War Domain",
        },
    },
    "druid": {
        "name": "Druid",
        "subclasses": {
            "druid_land": "Circle of the Land",
            "druid_moon": "Circle of the Moon",
        },
    },
    "fighter": {
        "name": "Fighter",
        "subclasses": {
            "fighter_champion": "Champion",
            "fighter_battle_master": "Battle Master",
            "fighter_eldritch_knight": "Eldritch Knight",
        },
    },
    "monk": {
        "name": "Monk",
        "subclasses": {
            "monk_open_hand": "Way of the Open Hand",
            "monk_shadow": "Way of Shadow",
            "monk_four_elements": "Way of the Four Elements",
        },
    },
    "paladin": {
        "name": "Paladin",
        "subclasses": {
            "paladin_devotion": "Oath of Devotion",
            "paladin_ancients": "Oath of the Ancients",
            "paladin_vengeance": "Oath of Vengeance",
        },
    },
    "ranger": {
        "name": "Ranger",
        "subclasses": {
            "ranger_hunter": "Hunter",
            "ranger_beast_master": "Beast Master",
        },
    },
    "rogue": {
        "name": "Rogue",
        "subclasses": {
            "rogue_thief": "Thief",
            "rogue_assassin": "Assassin",
            "rogue_arcane_trickster": "Arcane Trickster",
        },
    },
    "sorcerer": {
        "name": "Sorcerer",
        "subclasses": {
            "sorcerer_draconic_bloodline": "Draconic Bloodline",
            "sorcerer_wild_magic": "Wild Magic",
        },
    },
    "warlock": {
        "name": "Warlock",
        "subclasses": {
            "warlock_archfey": "The Archfey",
            "warlock_fiend": "The Fiend",
            "warlock_great_old_one": "The Great Old One",
        },
    },
    "wizard": {
        "name": "Wizard",
        "subclasses": {
            "wizard_abjuration": "School of Abjuration",
            "wizard_conjuration": "School of Conjuration",
            "wizard_divination": "School of Divination",
            "wizard_enchantment": "School of Enchantment",
            "wizard_evocation": "School of Evocation",
            "wizard_illusion": "School of Illusion",
            "wizard_necromancy": "School of Necromancy",
            "wizard_transmutation": "School of Transmutation",
        },
    },
}

CLASS_CHOICES = [(key, value["name"]) for key, value in CLASS_SUBCLASS_MAP.items()]
SUBCLASS_CHOICES = [
    (sub_key, sub_name)
    for cls in CLASS_SUBCLASS_MAP.values()
    for sub_key, sub_name in cls["subclasses"].items()
]

class CharacterStats(models.Model):
    strength = models.PositiveIntegerField(default=10)
    dexterity = models.PositiveIntegerField(default=10)
    constitution = models.PositiveIntegerField(default=10)
    intelligence = models.PositiveIntegerField(default=10)
    wisdom = models.PositiveIntegerField(default=10)
    charisma = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f"STR {self.strength}, DEX {self.dexterity}, CON {self.constitution}, " \
               f"INT {self.intelligence}, WIS {self.wisdom}, CHA {self.charisma}"


class Character(models.Model):
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
    subclass = models.CharField(max_length=50, choices=SUBCLASS_CHOICES, null=True, blank=True)
    race = models.CharField(max_length=20, choices=RACE_CHOICES)

    stats = models.OneToOneField(
        CharacterStats,
        on_delete=models.CASCADE,
        related_name="character"
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="characters"
    )

    def get_possible_spells(self):
        url = f"{settings.API_URL}/classes/{self.character_class}/"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            spells = data.get("possible_spells", [])
            return [s for s in spells if s.get("level", 0) <= self.level]
        return []

    def get_prepared_spells(self):
        possible_ids = {s["id"] for s in self.get_possible_spells()}
        return Spell.objects.filter(
            prepared_for_characters__character=self, id__in=possible_ids
        )

    def __str__(self):
        sub = f" ({self.subclass})" if self.subclass else ""
        return f"{self.name} the {self.race} {self.character_class.capitalize()}{sub} (Level {self.level})"



from spells.models import Spell


class PreparedSpell(models.Model):
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name="prepared_spells"
    )
    spell = models.ForeignKey(
        Spell,
        on_delete=models.CASCADE,
        related_name="prepared_for_characters"
    )

    class Meta:
        unique_together = ("character", "spell")

    def __str__(self):
        return f"{self.character.name} prepared {self.spell.name}"
