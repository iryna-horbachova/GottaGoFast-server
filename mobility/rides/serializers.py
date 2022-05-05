from rest_framework import serializers

from .models import RideRequest, DesignatedRide


class RideRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideRequest
        fields = ['id', 'client_id', 'start_location_latitude', 'start_location_longitude',
                  'end_location_latitude', 'end_location_longitude', 'adults_seats_number',
                  'children_seats_number', 'animal_seats_number', 'trunk_capacity',
                  'air_conditioner_present', 'timestamp']


class DesignatedRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignatedRide
        fields = ['driver_id', 'ride_request_id', 'price', 'status']