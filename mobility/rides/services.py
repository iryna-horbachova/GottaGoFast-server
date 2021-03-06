import requests
import datetime
from geopy import distance

from .models import RideRequest, DesignatedRide

from celery import Celery

from .storage import GeoStorageManager

app = Celery('mobility')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def schedule_designated_rides():
    print("designated rides")
    RidesDesignationManager().designate_rides()


class AuthenticationManager:

    BASE_URL = 'http://localhost:8000/api/profile/'
    USER_ID_ENDPOINT = 'user/id/'
    AUTHORIZATION_HEADER = 'Authorization'

    def get_user_id_or_none(self, headers):
        if self.AUTHORIZATION_HEADER not in headers:
            return None

        # Call authentication microservice
        url = self.BASE_URL + self.USER_ID_ENDPOINT
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

        return active_drivers_request.json()


    def matched_drivers_for_request(self, ride_request, drivers):
        matched_drivers = []

        for driver in drivers:
            if driver['vehicle']['adults_seats_number'] < ride_request.adults_seats_number or \
                driver['vehicle']['children_seats_number'] < ride_request.children_seats_number or \
                driver['vehicle']['animal_seats_number'] < ride_request.animal_seats_number or \
                driver['vehicle']['trunk_capacity'] < ride_request.trunk_capacity or \
                (not driver['vehicle']['air_conditioner_present'] and ride_request.air_conditioner_present):
                continue
            matched_drivers.append(driver)

        return matched_drivers


    def update_driver_status(self, driver_id):
        url = AuthenticationManager().BASE_URL + 'drivers/status/' + driver_id + '/'
        data = {'status': 'B'}
        driver_status_request = requests.post(url, data)
        print("Driver status", driver_status_request.status_code)


    def calculate_ride_cost_for_driver(self, ride_request, driver):
        BASE_RATE_PER_KM = 0.38

        # Check vehicle type
        if driver['vehicle']['type'] == 'M':
            BASE_RATE_PER_KM = 0.45
        elif driver['vehicle']['type'] == 'T':
            BASE_RATE_PER_KM = 0.5

        # Check vehicle category
        if driver['vehicle']['category'] == "E":
            BASE_RATE_PER_KM *= 0.85
        elif driver['vehicle']['category'] == "C":
            BASE_RATE_PER_KM *= 1.15

        # Check date
        weekday = datetime.datetime.today().weekday()

        if weekday == 5 or weekday == 6:
            BASE_RATE_PER_KM *= 1.17

        # Calculate distance between driver+start point, start point+end point
        start_point = (ride_request.start_location_latitude, ride_request.start_location_longitude)
        end_point = (ride_request.end_location_latitude, ride_request.end_location_longitude)
        ride_distance = distance.distance(start_point, end_point).km

        current_driver_geotag = GeoStorageManager.find_latest_user_location(driver['user']['id'])
        distance_to_start = 1

        if current_driver_geotag:
            current_driver_location = (current_driver_geotag['latitude'], current_driver_geotag['longitude'])
            distance_to_start = distance.distance(current_driver_location, start_point).km

        return round((BASE_RATE_PER_KM * ride_distance + BASE_RATE_PER_KM * 0.8 * distance_to_start) * 10, 2)

    def designate_rides(self):
        print("designate rides")
        # Create a set of requested ride that do not have an assignment yet
        already_designated_rides_ids = DesignatedRide.objects.values_list('ride_request_id', flat=True)

        ride_requests = list((RideRequest.objects.exclude(id__in=already_designated_rides_ids)))
        print("ride requests", ride_requests)
        if not ride_requests:
            return
        ride_requests.sort(key=lambda request: request.timestamp)

        # Get active drivers
        active_drivers = self.get_active_drivers()
        print("active drivers")
        print(active_drivers)
        if not active_drivers:
            return

        # Iterate through all ride requests
        for request in ride_requests:
            print("request", request)
            # Form a set of drivers that match condition
            matched_drivers = self.matched_drivers_for_request(request, active_drivers)

            if not matched_drivers:
                continue

            # Calculate cost of a ride for all available drivers
            cost_to_drivers = {}
            for driver in matched_drivers:
                cost_to_drivers[self.calculate_ride_cost_for_driver(request, driver)] = driver


            print("COST TO DRIVERS")
            print(cost_to_drivers)
            costs = list(cost_to_drivers.keys())
            minimum_cost = min(costs)
            #minimum_cost = min(cost_to_drivers, key=cost_to_drivers.get)
            DesignatedRide.objects.create(
                ride_request_id=request.id,
                driver_id=cost_to_drivers[minimum_cost]['user']['id'],
                price=minimum_cost
            )

            active_drivers.remove(cost_to_drivers[minimum_cost])




