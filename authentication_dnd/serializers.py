from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer

class CustomRegisterSerializer(RegisterSerializer):
    ROLE_CHOICES = [
        ('player', 'Player'),
        ('dm', 'Dungeon Master'),
    ]
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['role'] = self.validated_data.get('role', 'player')
        return data

    def get_response_data(self, user):
        data = super().get_response_data(user)
        data['role'] = user.role
        return data


class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data

from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers

class CustomUserDetailsSerializer(UserDetailsSerializer):
    role = serializers.CharField(source='role')

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('role',)
