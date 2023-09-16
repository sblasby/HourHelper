from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account_info")
    wage = models.FloatField()

    def __str__(self) -> str:
        return f'{self.user.first_name} makes {self.wage}$ an hour'

