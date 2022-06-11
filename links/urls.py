from django.urls import path
from .views import ListCreateLinksView, RetrieveUpdateDestroyLinkView

urlpatterns = [
    path("links/", ListCreateLinksView.as_view(), name="links"),
    path("link/<int:pk>/", RetrieveUpdateDestroyLinkView.as_view(), name="link"),
]