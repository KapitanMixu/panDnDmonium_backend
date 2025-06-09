from rest_framework import generics
from .models import Character
from .serializers import CharacterSerializer
from .permissions import IsPlayer

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
