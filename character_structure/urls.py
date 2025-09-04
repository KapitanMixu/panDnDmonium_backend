# character_structure/urls.py
from django.urls import path
from .views import (
    ClassListCreateView,
    ClassDetailView,
    ClassSubclassesListView,
    ClassSubclassDetailView,
)

urlpatterns = [
    path('classes/', ClassListCreateView.as_view(), name='class-list'),
    path('classes/<str:pk>/', ClassDetailView.as_view(), name='class-detail'),
    path('classes/<str:class_id>/subclasses/', ClassSubclassesListView.as_view(), name='class-subclass-list'),
    path('classes/<str:class_id>/subclasses/<str:id>/', ClassSubclassDetailView.as_view(), name='class-subclass-detail'),
]
