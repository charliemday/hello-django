from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Team, TeamMember
from .serializers import TeamSerializer

# Create your views here.


class TeamView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TeamSerializer

    def get_queryset(self):
        user = self.request.user
        teams = Team.objects.filter(members=user, is_active=True)
        return teams

    def create(self, request, *args, **kwargs):
        data = {**request.data}
        user = request.user

        data["created_by"] = user.id
        if data.get("members") is None:
            data["members"] = [user.id]

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
        user = self.request.user
        teams = Team.objects.filter(members=user, is_active=True)
        return teams

    def delete(self, request, *args, **kwargs):
        if self.get_object().created_by != self.request.user:
            return Response(
                {"message": "You cannot delete this team"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        team = self.get_object()
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)