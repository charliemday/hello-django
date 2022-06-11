from rest_framework import serializers

from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Team name must be at least 3 characters long.")
        return value

    def validate_members(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Team must have at least 1 member.")
        return value

    class Meta:
        model = Team
        fields = "__all__"


