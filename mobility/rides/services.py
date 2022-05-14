import requests
import json
import datetime
from geopy import distance
from types import SimpleNamespace

from .models import RideRequest, DesignatedRide


class AuthenticationManager:

    BASE_URL = 'http://localhost:8000/'
    USER_ID_ENDPOINT = 'api/profile/user/id/'
    AUTHORIZATION_HEADER = 'Authorization'

    def get_user_id_or_none(self, headers):
        if self.AUTHORIZATION_HEADER not in headers:
            return None

        # Call authentication microservice
        user_id_request = requests.get(url, headers=headers)

        if not user_id_request or user_id_request.status_code == 401:
            return None

        return user_id_request.json()['user_id']


class RidesDesignationManager:

    def get_active_drivers(self):
        url = AuthenticationManager().BASE_URL + 'drivers/active/'
        active_drivers_request = requests.get(url)
        if active_drivers_request.status_code != 200:
            return None

        x = json.loads(active_drivers_request.json(), object_hook=lambda d: SimpleNamespace(**d))
        return x

    def matched_drivers_for_request(self, ride_request, drivers):
        matched_drivers = []

        for driver in drivers:
            if driver.vehicle.adults_seats_number < ride_request.adults_seats_number or \
                driver.vehicle.children_seats_number < ride_request.children_seats_number or \
                driver.vehicle.animal_seats_number < ride_request.animal_seats_number or \
                driver.vehicle.trunk_capacity < ride_request.trunk_capacity or \
                (not driver.vehicle.air_conditioner_present and ride_request.air_conditioner_present):
                continue
            matched_drivers.append(driver)

        return matched_drivers

    def calculate_ride_cost_for_driver(self, ride_request, driver):
        BASE_RATE_PER_KM = 5

        # Check vehicle category
        if driver.vehicle.category == "E":
            BASE_RATE_PER_KM *= 0.85
        elif driver.vehicle.category == "C":
            BASE_RATE_PER_KM *= 1.15

        # Check date
        weekday = datetime.datetime.today().weekday()

        if weekday == 5 or weekday == 6:
            BASE_RATE_PER_KM *= 1.17

        # TO-DO: add driver distance to the start point

        # Calculate distance between start and end points
        start_point = (ride_request.start_location_latitude, ride_request.start_location_longitude)
        end_point = (ride_request.end_location_latitude, ride_request.end_location_longitude)
        ride_distance = distance.distance(start_point, end_point).km

        return BASE_RATE_PER_KM * ride_distance

    def designate_rides(self):
        # Create a set of requested ride that do not have an assignment yet
        already_designated_rides = DesignatedRide.objects.values_list('ride_request_id', flat=True)
        ride_requests = list((RideRequest.objects.in_bulk(already_designated_rides, field_name='id')).values())

        if not ride_requests:
            return
        ride_requests.sort(key=lambda request: request.timestamp)

        # Get active drivers
        active_drivers = self.get_active_drivers()
        if not active_drivers:
            return

        # Iterate through all ride requests
        for request in ride_requests:
            # Form a set of drivers that match condition
            matched_drivers = self.matched_drivers_for_request(request, active_drivers)

            if not matched_drivers:
                continue

            # Calculate cost of a ride for all available drivers
            cost_to_drivers = {}
            for driver in matched_drivers:
                cost_to_drivers[self.calculate_ride_cost_for_driver(driver)] = driver

            minimum_cost = min(cost_to_drivers, key=cost_to_drivers.get)
            d_ride = DesignatedRide.objects.create(
                ride_request_id=request.id,
                driver_id=cost_to_drivers[minimum_cost].id,
                price=minimum_cost
            )
            active_drivers.remove(cost_to_drivers[minimum_cost])




