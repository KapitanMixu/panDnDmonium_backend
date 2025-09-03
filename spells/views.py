import requests
from rest_framework import viewsets, decorators, response, status
from .models import Spell
from .serializers import SpellSerializer

class SpellViewSet(viewsets.ModelViewSet):
    queryset = Spell.objects.all().order_by("level", "name")
    serializer_class = SpellSerializer

    #view details action
    @decorators.action(detail=True, methods=["get"])
    def details(self, request, pk=None):
        spell = self.get_object()
        url = f"https://www.dnd5eapi.co/api/spells/{spell.api_id}"
        r = requests.get(url)

        if r.status_code != 200:
            return response.Response({"error": "Can't find details"},
                                     status=status.HTTP_502_BAD_GATEWAY)

        return response.Response(r.json())
