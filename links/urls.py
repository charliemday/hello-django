from django.urls import path
from .views import (
    ListCreateLinksView,
    RetrieveUpdateDestroyLinkView,
    ListCreateCategoriesView,
    RetrieveUpdateDestroyCategoryView,
)

urlpatterns = [
    path("links/", ListCreateLinksView.as_view(), name="links"),
    path("link/<int:pk>/", RetrieveUpdateDestroyLinkView.as_view(), name="link"),
    path("categories/", ListCreateCategoriesView.as_view(), name="categories"),
    path(
        "category/<int:pk>/",
        RetrieveUpdateDestroyCategoryView.as_view(),
        name="category",
    ),
]
