import random
import string
import uuid

from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=10, unique=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        
        super(Team, self).save(*args, **kwargs)

    
    def generate_unique_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase, string.digits, k=6))
            if not Team.objects.filter(code=code).exists():
                return code


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
