from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel

# Create your models here.

class User(AbstractUser):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserFeedback(TimeStampedModel):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _("User Feedback")
        verbose_name_plural = _("User Feedback")