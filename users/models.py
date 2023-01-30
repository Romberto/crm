from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    POSITIONS = (
        ('DR', 'директор'),
        ('MP', 'менеджер по продажам'),
        ('BG', 'бухгалтер'),
        ('MD', 'менеджер по работе с документами')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    position = models.CharField(max_length=40, choices=POSITIONS)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return str(f'{self.pk} user {self.user}')


