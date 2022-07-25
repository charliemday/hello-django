from unicodedata import category
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Link, LogoImage, Team
from .serializers import LinksSerializer, CategorySerializer
from .utils import extract_domain, request_brandfetch

from tempfile import NamedTemporaryFile
import os
from django.core.files import File
from urllib.request import urlopen

# Create your views here.


class ListCreateLinksView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = LinksSerializer

    def get_queryset(self):
        user = self.request.user
        links = Link.objects.filter(Q(team__team_members__user=user))
        return links

    def get(self, request, *args, **kwargs):
        team_param = request.GET.get("team")
        if team_param is None:
            return Response(
                {"message": "You must specify a team"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().get(request, *args, **kwargs)

    def create(self, request):

        data = {**request.data}
        user = request.user
        category_pk = request.data.get("category")

        team = get_object_or_404(Team, pk=request.data.get("team"))

        if not team.team_members.filter(user=user.pk).exists():
            return Response(
                {"message": "You must be part of the team to create links hello"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if category_pk is not None:
            category = get_object_or_404(Category, pk=category_pk)
            if not category.team.pk == team.pk:
                return Response(
                    {"message": "You must use one of your Team's categories"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data["created_by"] = user.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Here we want to check if the link already has a logo associated to it's domain

        url = data.get("url")
        domain = extract_domain(url)

        if domain is not None:
            logo = LogoImage.objects.filter(domain=domain).exists()
            if logo:
                logo = LogoImage.objects.get(domain=domain)
                serializer.instance.logo = logo
                serializer.instance.save()
            else:
                brandfetch_logo = request_brandfetch(domain)
                if brandfetch_logo is not None:

                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(urlopen(brandfetch_logo).read())
                    img_temp.flush()

                    _, file_extension = os.path.splitext(brandfetch_logo)

                    logo = LogoImage(domain=domain)
                    logo.image.save(
                        "{}{}".format(domain, file_extension), File(img_temp)
                    )
                    logo.save()

                    serializer.instance.logo = logo
                    serializer.instance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyLinkView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = LinksSerializer

    def get_queryset(self):
        links = Link.objects.filter(team__team_members__user=self.request.user)
        return links

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        team = instance.team

        if team.team_members.filter(user=self.request.user.pk).exists():
            id = instance.pk
            self.perform_destroy(instance)
            return Response({"id": id}, status=status.HTTP_200_OK)

        return Response(
            {"message": "You must be part of the team to delete links"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ListCreateCategoriesView(ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        categories = Category.objects.filter(team__team_members__user=user)
        return categories

    def get(self, request, *args, **kwargs):
        team_param = request.GET.get("team")
        if team_param:
            qs = Category.objects.filter(team=team_param)
            serializer = self.get_serializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        user = request.user
        team = get_object_or_404(Team, pk=request.data.get("team"))
        if team.team_members.filter(user=user.pk).exists():
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"message": "You must be a member of the team to create a category"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class RetrieveUpdateDestroyCategoryView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user
        categories = Category.objects.filter(team__team_members__user=user)
        return categories

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        team = instance.team

        if team.team_members.filter(user=self.request.user.pk).exists():
            id = instance.pk
            self.perform_destroy(instance)
            return Response({"id": id}, status=status.HTTP_200_OK)

        return Response(
            {"message": "You must be part of the team to delete categories"},
            status=status.HTTP_400_BAD_REQUEST,
        )
