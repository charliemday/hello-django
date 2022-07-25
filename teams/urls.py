from django.urls import path

from .views import (
    TeamView,
    RetrieveUpdateDestroyTeamView,
    TeamInviteView,
    CreateListTeamMemberView,
    RetrieveUpdateDestroyTeamMemberView,
    AcceptTeamInvite,
)

urlpatterns = [
    path("teams/", TeamView.as_view(), name="team"),
    path("team/<int:pk>/", RetrieveUpdateDestroyTeamView.as_view(), name="team"),
    path("team-invite/", TeamInviteView.as_view(), name="team-invite"),
    path("team-member/", CreateListTeamMemberView.as_view(), name="team-member"),
    path("team-member/<int:pk>/", RetrieveUpdateDestroyTeamMemberView.as_view(), name="team-member"),
    path("accept-invite/", AcceptTeamInvite.as_view(), name="accept-invite"),
]
