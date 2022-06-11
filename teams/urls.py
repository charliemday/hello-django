from django.urls import path

from .views import TeamView, RetrieveUpdateDestroyTeamView

urlpatterns = [
    path("teams/", TeamView.as_view(), name="team"),
    path("team/<int:pk>/", RetrieveUpdateDestroyTeamView.as_view(), name="team"),
]