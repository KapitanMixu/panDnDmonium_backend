from rest_framework import serializers
from .models import Character, CharacterStats, CLASS_SUBCLASS_MAP
from spells.models import Spell


class CharacterStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterStats
        fields = [
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
        ]


class SpellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spell
        fields = ["id", "name", "level", "ritual", "concentration", "components", "casting_time"]


class CharacterSerializer(serializers.ModelSerializer):
    stats = CharacterStatsSerializer()
    possible_spells = serializers.SerializerMethodField()
    prepared_spells = serializers.SerializerMethodField()

    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "level",
            "character_class",
            "subclass",
            "race",
            "stats",
            "owner",
            "possible_spells",
            "prepared_spells",
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
        stats_data = validated_data.pop("stats")
        stats = CharacterStats.objects.create(**stats_data)
        return Character.objects.create(stats=stats, **validated_data)

    def update(self, instance, validated_data):
        stats_data = validated_data.pop("stats", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if stats_data:
            for attr, value in stats_data.items():
                setattr(instance.stats, attr, value)
            instance.stats.save()
        return instance

    def get_possible_spells(self, obj):
        return obj.get_possible_spells()

    def get_prepared_spells(self, obj):
        spells = obj.get_prepared_spells()
        return SpellSerializer(spells, many=True).data
