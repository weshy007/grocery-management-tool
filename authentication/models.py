from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class Team(models.Model):
    code = models.CharField(max_length=10, unique=True)


class User(AbstractUser):
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
