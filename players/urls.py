from django.urls import path
from .views import CharacterCreateView, CharacterListView

urlpatterns = [
    path('characters/create/', CharacterCreateView.as_view(), name='character-create'),
    path('characters/', CharacterListView.as_view(), name='character-list'),
]
