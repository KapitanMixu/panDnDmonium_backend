from rest_framework import serializers
from .models import Class, Subclass, SubclassSpell
from spells.serializers import SpellSerializer


class SubclassSpellSerializer(serializers.ModelSerializer):
    spell = SpellSerializer()

    class Meta:
        model = SubclassSpell
        fields = ["level_granted", "always_prepared", "spell"]


class SubclassSerializer(serializers.ModelSerializer):
    parent_class = serializers.SerializerMethodField()
    subclass_spells = SubclassSpellSerializer(many=True, read_only=True)

    class Meta:
        model = Subclass
        fields = ["id", "name", "parent_class", "subclass_spells"]

    def get_parent_class(self, obj):
        return [cls.name for cls in obj.class_set.all()]


class ClassSerializer(serializers.ModelSerializer):
    possible_spells = SpellSerializer(many=True, read_only=True)
    subclasses = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="id"
    )

    class Meta:
        model = Class
        fields = ['id', 'name', 'subclasses', 'possible_spells']
