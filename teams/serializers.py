from rest_framework import serializers

from .models import Team, TeamInvite, TeamMember

from users.serializers import UserSerializer

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):

    members = serializers.SerializerMethodField(read_only=True)

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Team name must be at least 3 characters long.")
        return value

    def validate_members(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("Team must have at least 1 member.")
        return value

    def get_members(self, obj):
        members = obj.team_members.all()
        formatted_members = []
        for member in members:
            formatted_members.append({
                **UserSerializer(member.user).data,
                "team_member_id": member.id,
            })
        return formatted_members

    class Meta:
        model = Team
        fields = "__all__"

class TeamInviteSerializer(serializers.ModelSerializer):

    token = serializers.CharField(read_only=True)

    class Meta:
        model = TeamInvite
        fields = "__all__"