from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Team, TeamMember, TeamInvite
from .serializers import TeamSerializer, TeamInviteSerializer, TeamMemberSerializer

from .utils import send_simple_message

# Create your views here.


class TeamView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer

    def get_queryset(self):
        user = self.request.user
        user_team_members = TeamMember.objects.filter(
            user=user,
            is_active=True
        )
        return [member.team for member in user_team_members]

    def create(self, request, *args, **kwargs):
        data = {**request.data}
        user = request.user

        data["created_by"] = user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Additionally create first team member which will be this user
        TeamMember.objects.create(team=serializer.instance, user=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyTeamView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer

    def get_queryset(self):
        """
        Only query the teams that the user is a team member of
        """
        user_team_members = TeamMember.objects.filter(
            user=self.request.user,
            is_active=True
        )

        return Team.objects.filter(team_members__in=user_team_members)

    def delete(self, request, *args, **kwargs):
        """
        Only allow the owner of the team to delete it
        """
        if self.get_object().created_by != self.request.user:
            return Response(
                {"message": "You cannot delete this team"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        team = self.get_object()
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateListTeamMemberView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TeamMemberSerializer

    def get_queryset(self):
        return TeamMember.objects.filter(team__members=self.request.user)

    def get(self, request, *args, **kwargs):
        team_param = request.GET.get("team")
        if team_param is None:
            return Response(
                {"message": "You must specify a team"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().get(request, *args, **kwargs)

class RetrieveUpdateDestroyTeamMemberView(RetrieveUpdateDestroyAPIView):
    
    def get_queryset(self):
        return TeamMember.objects.filter(team__team_members__user=self.request.user)

    def delete(self, request, *args, **kwargs):
        """
        Only allow the owner of the team to remove team members
        """
        if self.get_object().team.created_by != self.request.user:
            return Response(
                {"message": "Only the owner can remove team members"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        team = self.get_object()
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TeamInviteView(CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TeamInviteSerializer

    def create(self, request, *args, **kwargs):
        data = {**request.data}
        user = request.user

        data["created_by"] = user.id

        email = data.get("email")

        print("=======")
        print("[FAKE] Sending invite to:", email)
        send_simple_message(email)
        print("=======")

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AcceptTeamInvite(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Accept the team invitation by first verifying this is
        a valid invitation token and then adding to the team
        """
        token = request.data.get("token")
        user = request.user

        if token is None:
            return Response(
                {"message": "No token provided"}, status=status.HTTP_400_BAD_REQUEST,
            )

        # Check this is a valid token
        team_invite = get_object_or_404(TeamInvite, token=token)

        team = team_invite.team

        # Check they're not already a member of this team
        existing_team_member = TeamMember.objects.filter(user=user).exists()

        if not existing_team_member:
            # Add them to the team
            new_team_member = TeamMember.objects.create(user=user, team=team)
            new_team_member.save()
            team_invite.delete()

        return Response({"message": "Invite accepted"}, status=status.HTTP_201_CREATED)

