from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Character, PreparedSpell
from .serializers import CharacterSerializer
from .permissions import IsPlayer
from spells.models import Spell


class CharacterCreateView(generics.CreateAPIView):
    serializer_class = CharacterSerializer
    permission_classes = [IsPlayer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CharacterListView(generics.ListAPIView):
    serializer_class = CharacterSerializer
    permission_classes = [IsPlayer]

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)


class CharacterDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CharacterSerializer
    permission_classes = [IsPlayer]

    def get_queryset(self):
        return Character.objects.filter(owner=self.request.user)


class AddPreparedSpellView(APIView):
    permission_classes = [IsPlayer]

    def post(self, request, pk):
        """Dodaje przygotowany czar do postaci"""
        try:
            character = Character.objects.get(pk=pk, owner=request.user)
        except Character.DoesNotExist:
            return Response({"error": "Character not found"}, status=status.HTTP_404_NOT_FOUND)

        spell_id = request.data.get("spell_id")
        try:
            spell = Spell.objects.get(id=spell_id)
        except Spell.DoesNotExist:
            return Response({"error": "Spell not found"}, status=status.HTTP_404_NOT_FOUND)

        # sprawdź czy spell pasuje do klasy/poziomu
        possible_ids = {s["id"] for s in character.get_possible_spells()}
        if spell.id not in possible_ids:
            return Response(
                {"error": "This spell is not available for this character"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        PreparedSpell.objects.get_or_create(character=character, spell=spell)
        return Response({"status": f"{spell.name} prepared"}, status=status.HTTP_201_CREATED)


class RemovePreparedSpellView(APIView):
    permission_classes = [IsPlayer]

    def delete(self, request, pk, spell_id):
        """Usuwa przygotowany czar z postaci"""
        try:
            character = Character.objects.get(pk=pk, owner=request.user)
        except Character.DoesNotExist:
            return Response({"error": "Character not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            prepared = PreparedSpell.objects.get(character=character, spell_id=spell_id)
            prepared.delete()
            return Response({"status": "Spell unprepared"}, status=status.HTTP_200_OK)
        except PreparedSpell.DoesNotExist:
            return Response({"error": "Not prepared"}, status=status.HTTP_404_NOT_FOUND)
