from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator


class RideRequest(models.Model):
    client_id = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=False,
        blank=False
    )
    start_location_latitude = models.FloatField(default=0)
    start_location_longitude = models.FloatField(default=0)
    end_location_latitude = models.FloatField(default=0)
    end_location_longitude = models.FloatField(default=0)

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

    timestamp = models.DateTimeField(auto_now_add=True)


class DesignatedRide(models.Model):

    class Statuses(models.TextChoices):
        AWAITING = 'A', _('Awaiting')
        IN_PROGRESS = 'I', _('In progress')
        FINISHED = 'F', _('Finished')
        CANCELLED = 'C', _('Cancelled')

    driver_id = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=False,
        blank=False
    )
    ride_request_id = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=False,
        blank=False
    )
    price = models.FloatField(validators=[MinValueValidator(0)], default=0)
    status = models.CharField(
        _('status'),
        choices=Statuses.choices,
        max_length=1,
        default="A"
    )
