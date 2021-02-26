from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email address', max_length=255, unique=True)
    
    def is_subscribe(self, user):
         return self.follower.filter(user=user).exists()
