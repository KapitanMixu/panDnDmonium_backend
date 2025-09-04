from rest_framework import generics
from .models import Class, Subclass
from .serializers import ClassSerializer, SubclassSerializer
from rest_framework.exceptions import NotFound


class ClassListCreateView(generics.ListCreateAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer


class ClassSubclassesListView(generics.ListAPIView):
    serializer_class = SubclassSerializer

    def get_queryset(self):
        class_id = self.kwargs["class_id"]
        try:
            class_obj = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            raise NotFound(detail=f"Class '{class_id}' does not exist.")
        return class_obj.subclasses.all()


class ClassSubclassDetailView(generics.RetrieveAPIView):
    serializer_class = SubclassSerializer
    lookup_field = "id"
    queryset = Subclass.objects.all()

    def get_queryset(self):
        class_id = self.kwargs["class_id"]
        try:
            class_obj = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            raise NotFound(detail=f"Class '{class_id}' does not exist.")
        return class_obj.subclasses.all()
