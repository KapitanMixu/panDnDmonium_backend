from rest_framework import serializers
from .models import Character, CLASS_SUBCLASS_MAP


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "level",
            "character_class",
            "subclass",
            "race",
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
            "owner",
        ]
        read_only_fields = ["owner"]

    def validate_subclass(self, value):
        character_class = self.initial_data.get("character_class")
        if value and character_class:
            valid_subclasses = CLASS_SUBCLASS_MAP.get(character_class, {}).get("subclasses", {}).keys()
            if value not in valid_subclasses:
                raise serializers.ValidationError(
                    f"Invalid subclass for {character_class}. "
                    f"Valid options: {list(valid_subclasses)} or None."
                )
        return value

    def create(self, validated_data):
        return Character.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
