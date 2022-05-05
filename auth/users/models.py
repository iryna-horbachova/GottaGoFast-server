from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from .managers import UserManager


class User(AbstractUser):
    class Genders(models.TextChoices):
        FEMALE = 'F', _('Female')
        MALE = 'M', _('Male')
        UNKNOWN = 'U', _('Unknown')

    username = None
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    gender = models.CharField(
        _('gender'),
        choices=Genders.choices,
        max_length=1,
        default="U"
    )
    phone_number = models.CharField(_('phone number'), max_length=25)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)

    admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    ride_discount = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Vehicle(models.Model):
    class Types(models.TextChoices):
        PASSENGER = 'P', _('Passenger')
        TRUCK = 'T', _('Truck')
        MINIVAN = 'M', _('Minivan')

    model = models.CharField(_('model'), max_length=25)
    type = models.CharField(_('type'), choices=Types.choices, max_length=25)
    insurance_policy_number = models.CharField(_('insurance policy number'), max_length=25)
    adults_seats_number = models.IntegerField(
        _('adults seats number'), default=0,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(0)
        ]
    )
    children_seats_number = models.IntegerField(
        _('children seats number'), default=0,
        validators=[
            MaxValueValidator(50),
            MinValueValidator(0)
        ]
    )
    animal_seats_number = models.IntegerField(
        _('animal seats number'), default=0,
        validators=[
            MaxValueValidator(50),
            MinValueValidator(0)
        ]
    )
    trunk_capacity = models.IntegerField(
        _('trunk capacity'), default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ]
    )
    air_conditioner_present = models.BooleanField(_('air conditioner present'), default=False)


class Driver(models.Model):
    class Statuses(models.TextChoices):
        NOT_VERIFIED = 'N', _('Not verified')
        INACTIVE = 'I', _('Inactive')
        ACTIVE = 'A', _('Active')
        BUSY = 'B', _('Busy')

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    vehicle = models.OneToOneField(
        Vehicle,
        on_delete=models.CASCADE,
        null=True
    )
    passport_number = models.CharField(_('passport number'), max_length=25)
    driver_license_number = models.CharField(_('driver license number'), max_length=25)
    taxi_license_number = models.CharField(_('taxi license number'), max_length=25)
    status = models.CharField(
        _('status'),
        choices=Statuses.choices,
        max_length=1,
        default="N"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"