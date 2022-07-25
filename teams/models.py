import uuid
from django.db import models
from django_extensions.db.models import TimeStampedModel

from users.models import User

# Create your models here.

class Team(TimeStampedModel):

    name = models.CharField(max_length=200)

    description = models.TextField(max_length=200, default=None, blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class TeamMember(TimeStampedModel):

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_members")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username 


class TeamInvite(TimeStampedModel):

    token = models.UUIDField(default=uuid.uuid4)

    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    email = models.EmailField(default=None, blank=True, null=True)

    def __str__(self) -> str:
        return "{} ({})".format(self.token, self.team)