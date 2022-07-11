from django.db.models import Q

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Link, LogoImage
from .serializers import LinksSerializer
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
        links = Link.objects.filter(Q(team__members=user) | Q(created_by=user))
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
                    logo.image.save('{}{}'.format(domain, file_extension), File(img_temp))
                    logo.save()

                    serializer.instance.logo = logo
                    serializer.instance.save()


        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyLinkView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = LinksSerializer

    def get_queryset(self):
        links = Link.objects.filter(team__members=self.request.user)
        return links

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        id = instance.pk
        self.perform_destroy(instance)
        return Response({"id": id}, status=status.HTTP_200_OK)
