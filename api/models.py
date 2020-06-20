from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from django.db import models

class Role(models.TextChoices):
    USER = 'U', _('user')
    MODERATOR = 'M', _('moderator')
    ADMIN = 'A', _('admin')

class ClientManager(UserManager):
    def _create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        confirmation_code = get_random_string()
        client = self.model(
            username=username,
            email=email,
            confirmation_code=confirmation_code,
            **extra_fields
        )
        client.set_password(password)
        client.save(using=self._db)
        return client

    def create_user(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(self, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('role', Role.ADMIN)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, password, **extra_fields)

class Client(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True,
        null=True,
    )
    role = models.CharField(
        max_length=1,
        choices=Role.choices,
        default=Role.USER,
    )
    bio = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=12, null=True)
    objects = ClientManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
