# management/commands/import_phb_classes.py
from django.core.management.base import BaseCommand
from character_structure.models import Class, Subclass

class Command(BaseCommand):
    help = "Create DnD PHB classes and their subclasses"

    # PHB classes and their subclasses
    classes_with_subclasses = {
        "barbarian": ["Path of the Berserker", "Path of the Totem Warrior"],
        "bard": ["College of Lore", "College of Valor"],
        "cleric": [
            "Knowledge Domain", "Life Domain", "Light Domain",
            "Nature Domain", "Tempest Domain", "Trickery Domain", "War Domain"
        ],
        "druid": ["Circle of the Land", "Circle of the Moon"],
        "fighter": ["Champion", "Battle Master", "Eldritch Knight"],
        "monk": ["Way of the Open Hand", "Way of Shadow", "Way of the Four Elements"],
        "paladin": ["Oath of Devotion", "Oath of the Ancients", "Oath of Vengeance"],
        "ranger": ["Hunter", "Beast Master"],
        "rogue": ["Thief", "Assassin", "Arcane Trickster"],
        "sorcerer": ["Draconic Bloodline", "Wild Magic"],
        "warlock": ["The Archfey", "The Fiend", "The Great Old One"],
        "wizard": [
            "School of Abjuration", "School of Conjuration", "School of Divination",
            "School of Enchantment", "School of Evocation", "School of Illusion",
            "School of Necromancy", "School of Transmutation"
        ]
    }

    def handle(self, *args, **options):
        for class_id, subclass_names in self.classes_with_subclasses.items():
            # Create Class
            class_obj, created = Class.objects.get_or_create(
                id=class_id,
                defaults={'name': class_id.capitalize()}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Created class: {class_obj.name}"))
            else:
                self.stdout.write(f"ℹ️ Class already exists: {class_obj.name}")

            # Create Subclasses
            for sub_name in subclass_names:
                sub_id = sub_name.lower().replace(" ", "_")  # e.g., "Path of the Berserker" -> "path_of_the_berserker"
                subclass_obj, created = Subclass.objects.get_or_create(
                    id=sub_id,
                    defaults={'name': sub_name}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ Created subclass: {sub_name}"))
                else:
                    self.stdout.write(f"ℹ️ Subclass already exists: {sub_name}")

                # Assign subclass to class (many-to-many)
                if subclass_obj not in class_obj.subclasses.all():
                    class_obj.subclasses.add(subclass_obj)
                    self.stdout.write(self.style.SUCCESS(f"✅ Assigned {sub_name} to {class_obj.name}"))

        self.stdout.write(self.style.SUCCESS("✅ All PHB classes and subclasses created successfully"))
