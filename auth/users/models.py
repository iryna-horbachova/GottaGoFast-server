from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser):

    class Genders(models.TextChoices):
        FEMALE = 'F', _('Female')
        MALE = 'M', _('Male')
        UNKNOWN = 'U', _('Unknown')

    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    gender = models.CharField(
        _('first name'),
        choices=Genders.choices,
        max_length=1,
        default="U"
    )
    phone_number = models.CharField(_('phone number'), max_length=25)
    birth_date = models.DateField(null=True, blank=True)

    admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
