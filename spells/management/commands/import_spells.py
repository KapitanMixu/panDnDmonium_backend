import requests
from django.core.management.base import BaseCommand
from spells.models import Spell

class Command(BaseCommand):
    help = "Imports spells from the DnD 5e API (light version)"

    def handle(self, *args, **kwargs):
        base_url = "https://www.dnd5eapi.co"
        list_url = f"{base_url}/api/spells"

        # Get the list of all spells
        r = requests.get(list_url)
        data = r.json()

        for s in data["results"]:
            # Fetch spell details (contains level, school, ritual, etc.)
            details_url = f"{base_url}{s['url']}"
            details = requests.get(details_url).json()

            # Save or update the spell in the database
            Spell.objects.update_or_create(
                id=s["index"],
                defaults={
                    "name": s["name"],
                    "level": details.get("level", 0),
                    "school": details.get("school", {}).get("name", None),
                    "ritual": details.get("ritual", False),
                    "concentration": details.get("concentration", False),
                    "components": details.get("components", []),
                }
            )

        self.stdout.write(self.style.SUCCESS("Spells successfully updated"))
