from unicodedata import category
from django.db import models
from django_extensions.db.models import TimeStampedModel

from users.models import User
from teams.models import Team

# Create your models here.

class LogoImage(TimeStampedModel):

    image = models.ImageField(upload_to='logo_images')

    domain = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.domain

class Category(TimeStampedModel):

    name = models.CharField(max_length=200)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'

    def __str__(self):
        return self.name

class Link(TimeStampedModel):

    name = models.CharField(max_length=200)

    description = models.TextField(max_length=200, default=None, blank=True, null=True)

    url = models.URLField(max_length=200)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)

    logo = models.ForeignKey(LogoImage, on_delete=models.CASCADE, null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

