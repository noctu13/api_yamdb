from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.db import models


class Client(AbstractUser):

    class Role(models.TextChoices):
        ANONYM = 'AN', _('Anonym')
        USER = 'US', _('User')
        MODERATOR = 'MO', _('Moderator')
        ADMIN = 'AD', _('Admin')
        DJANGO_ADMIN = 'DA', _('Django admin')

    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.USER,
    )

    def __str__(self):
        return self.username
