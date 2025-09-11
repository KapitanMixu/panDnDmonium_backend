from django.urls import path
from .views import (
    CharacterCreateView,
    CharacterListView,
    CharacterDetailView,
    AddPreparedSpellView,
    RemovePreparedSpellView,
)

urlpatterns = [
    path("characters/", CharacterListView.as_view(), name="character-list"),
    path("characters/create/", CharacterCreateView.as_view(), name="character-create"),
    path("characters/<int:pk>/", CharacterDetailView.as_view(), name="character-detail"),
    path("characters/<int:pk>/prepared_spells/", AddPreparedSpellView.as_view(), name="add-prepared-spell"),
    path("characters/<int:pk>/prepared_spells/<str:spell_id>/", RemovePreparedSpellView.as_view(), name="remove-prepared-spell"),
]
