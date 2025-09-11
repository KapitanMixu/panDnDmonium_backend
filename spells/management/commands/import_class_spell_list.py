# character_structure/management/commands/import_class_spells.py
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from character_structure.models import Class, Subclass, SubclassSpell
from spells.models import Spell


class Command(BaseCommand):
    help = "Import spells for classes and PHB subclasses"

    classes = ["cleric", "paladin", "warlock", "bard", "druid", "wizard", "ranger", "sorcerer"]

    # Manual PHB subclass spells
    subclasses_manual = {
        "cleric_knowledge_domain": {
            "1": ["command", "identify"],
            "3": ["augury", "suggestion"],
            "5": ["nondetection", "speak-with-dead"],
            "7": ["arcane-eye", "confusion"],
            "9": ["legend-lore", "scrying"]
        },
        "cleric_life_domain": {
            "1": ["bless", "cure-wounds"],
            "3": ["lesser-restoration", "spiritual-weapon"],
            "5": ["beacon-of-hope", "revivify"],
            "7": ["death-ward", "guardian-of-faith"],
            "9": ["mass-cure-wounds", "raise-dead"]
        },
        "cleric_light_domain": {
            "1": ["burning-hands", "faerie-fire"],
            "3": ["flaming-sphere", "scorching-ray"],
            "5": ["daylight", "fireball"],
            "7": ["guardian-of-faith", "wall-of-fire"],
            "9": ["flame-strike", "scrying"]
        },
        "cleric_nature_domain": {
            "1": ["animal-friendship", "speak-with-animals"],
            "3": ["barkskin", "spike-growth"],
            "5": ["plant-growth", "wind-wall"],
            "7": ["dominate-beast", "freedom-of-movement"],
            "9": ["insect-plague", "tree-stride"]
        },
        "cleric_tempest_domain": {
            "1": ["fog-cloud", "thunderwave"],
            "3": ["gust-of-wind", "shatter"],
            "5": ["call-lightning", "searing-smite"],
            "7": ["storm-sphere", "thunderous-smite"],
            "9": ["destructive-wave", "control-winds"]
        },
        "cleric_trickery_domain": {
            "1": ["disguise-self", "silent-image"],
            "3": ["mirror-image", "pass-without-trace"],
            "5": ["blink", "dispel-magic"],
            "7": ["dimension-door", "polymorph"],
            "9": ["dominate-person", "modify-memory"]
        },
        "cleric_war_domain": {
            "1": ["divine-favor", "shield-of-faith"],
            "3": ["magic-weapon", "spiritual-weapon"],
            "5": ["crusader's-mantle", "flame-strike"],
            "7": ["stoneskin", "spirit-guardians"],
            "9": ["hold-monster", "destructive-wave"]
        },
        "paladin_oath_of_devotion": {
            "3": ["protection-from-evil-and-good", "sanctuary"],
            "5": ["lesser-restoration", "zone-of-truth"],
            "9": ["beacon-of-hope", "dispel-magic"],
            "13": ["freedom-of-movement", "guardian-of-faith"],
            "17": ["commune", "flame-strike"]
        },
        "paladin_oath_of_the_ancients": {
            "3": ["ensnaring-strike", "speak-with-animals"],
            "5": ["moonbeam", "misty-step"],
            "9": ["plant-growth", "protection-from-energy"],
            "13": ["ice-storm", "stoneskin"],
            "17": ["commune-with-nature", "tree-stride"]
        },
        "paladin_oath_of_vengeance": {
            "3": ["bane", "hunters-mark"],
            "5": ["hold-person", "misty-step"],
            "9": ["haste", "protection-from-energy"],
            "13": ["banishment", "dimension-door"],
            "17": ["hold-monster", "scrying"]
        }
    }
    # Missing PHB spells for subclasses
    missing_spells = {
        # Cleric Domains
        "tempest_domain": [
            "searing-smite",
            "storm-sphere",
            "thunderous-smite",
            "destructive-wave",
            "control-winds"
        ],
        "war_domain": [
            "crusader's-mantle",
            "destructive-wave"
        ],

        # Paladin Oaths
        "oath_of_the_ancients": [
            "ensnaring-strike"
        ],

        # Rogue archetypes
        "arcane_trickster": [
            # fill manually if needed
        ],

        # Fighter archetypes
        "eldritch_knight": [
            # fill manually if needed
        ]
    }

    def handle(self, *args, **options):
        for cls_name in self.classes:
            try:
                cls_obj = Class.objects.get(id=cls_name)
            except Class.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠️ Class {cls_name} not found, skipping"))
                continue

            url = f"{settings.DND5E_API_BASE_URL}/api/classes/{cls_name}/spells"
            self.stdout.write(f"📥 Fetching spells for class {cls_name} → {url}")

            try:
                res = requests.get(url)
                res.raise_for_status()
                payload = res.json()
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️ Failed to fetch class spells: {e}"))
                continue

            results = payload.get("results", [])
            self.stdout.write(f"🔹 Found {len(results)} spells for class {cls_name}")

            for sp in results:
                spell_url = f"{settings.DND5E_API_BASE_URL}{sp['url']}"
                try:
                    res_sp = requests.get(spell_url)
                    res_sp.raise_for_status()
                    details = res_sp.json()
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️ Failed to fetch spell {sp['index']}: {e}"))
                    continue

                desc = details.get("desc", [])
                if isinstance(desc, list):
                    desc = " ".join(desc)

                spell_obj, created = Spell.objects.update_or_create(
                    id=details['index'],
                    defaults={
                        'name': details.get('name', ''),
                        'level': details.get('level', 0),
                        'ritual': details.get('ritual', False),
                        'concentration': details.get('concentration', False),
                        'components': details.get('components', []),
                        'casting_time': details.get('casting_time', ''),
                        'description': desc
                    }
                )
                cls_obj.possible_spells.add(spell_obj)
                if created:
                    self.stdout.write(f"✅ Created spell {spell_obj.name} for class {cls_name}")
                else:
                    self.stdout.write(f"ℹ️ Updated spell {spell_obj.name} for class {cls_name}")

            self.stdout.write(self.style.SUCCESS(f"🏆 Finished assigning spells for class {cls_name}"))


        for subclass_id, levels in self.subclasses_manual.items():
            # strip everything up to first underscore
            db_sub_id = "_".join(subclass_id.split("_")[1:])

            try:
                sub_obj = Subclass.objects.get(id=db_sub_id)
            except Subclass.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"⚠️ Subclass {db_sub_id} not found, skipping"))
                continue

            for lvl, spells in levels.items():
                # skip non-level keys like "allowed_schools" / "exceptions"
                if lvl in ("allowed_schools", "exceptions"):
                    continue

                for sp in spells:
                    try:
                        spell_obj = Spell.objects.get(id=sp)
                    except Spell.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"⚠️ Spell {sp} not found in DB, skipping"))
                        continue

                    SubclassSpell.objects.update_or_create(
                        subclass=sub_obj,
                        spell=spell_obj,
                        defaults={
                            "level_granted": int(lvl),
                            "always_prepared": sub_obj.id.startswith("cleric") or sub_obj.id.startswith("paladin")
                        }
                    )

            self.stdout.write(self.style.SUCCESS(f"✅ Assigned subclass spells for {db_sub_id}"))

        self.stdout.write(self.style.SUCCESS("🎯 All class and subclass spells imported successfully"))