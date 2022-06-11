from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Link
from .serializers import LinksSerializer

# Create your views here.


class ListCreateLinksView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = LinksSerializer
    queryset = Link.objects.all()

    def get(self, request, *args, **kwargs):
        team_param = request.GET.get("team")
        if team_param is None:
            return Response(
                {"message": "You must specify a team"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        data = {**request.data}
        user = request.user

        data["created_by"] = user

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyLinkView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = LinksSerializer

    def get_queryset(self):
        links = Link.objects.filter(team__members=self.request.user)
        return links


    # def update(self, request, *args, **kwargs):

    #     user = request.user
    #     link = self.get_object()

    #     if not link.team.members.filter(id=user.id).exists():
    #         return Response(
    #             {"message": "You do not have access to this team"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     return super().update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):

    #     user = request.user
    #     link = self.get_object()

    #     if not link.team.members.filter(id=user.id).exists():
    #         return Response(
    #             {"message": "You do not have access to this team"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     return super().destroy(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):

    #     user = request.user
    #     link = self.get_object()
    #     if not link.team.members.filter(id=user.id).exists():
    #         return Response(
    #             {"message": "You do not have access to this team"},
    #             status=status.HTTP_400_BAD_REQUEST,
    #         )

    #     return super().get(request, *args, **kwargs)

