from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='E-mail', max_length=255, unique=True)

    def is_subscribe(self, author):
        return self.follower.filter(author=author).exists()
