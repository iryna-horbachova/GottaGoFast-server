from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

from datetime import datetime

from .models import (
    RideRequest,
    DesignatedRide
)
from .serializers import (
    RideRequestSerializer,
    DesignatedRideSerializer
)
from .services import AuthenticationManager
from .storage import GeoStorageManager


class RideRequestListCreateAPIView(ListCreateAPIView):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer

    def check_permissions(self, request):
        if not AuthenticationManager().get_user_id(headers=request.headers):
            self.permission_denied(request)


class RideRequestReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer

    def check_permissions(self, request):
        if not AuthenticationManager().get_user_id(headers=request.headers):
            self.permission_denied(request)


class DesignatedRideReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = DesignatedRide.objects.all()
    serializer_class = DesignatedRideSerializer

    def check_permissions(self, request):
        if not AuthenticationManager().get_user_id(headers=request.headers):
            self.permission_denied(request)


@api_view(http_method_names=['GET'])
def get_designated_ride_statuses(request):
    statuses = [{'db_value': status[0], 'title': status[1]} for status in DesignatedRide.Statuses.choices]
    return Response(statuses)


@api_view(http_method_names=['GET'])
def get_designation_for_requested_ride(request, requested_ride_id):
    designated_ride = DesignatedRide.objects.filter(ride_request_id=requested_ride_id).first()
    serialized_data = None

    if designated_ride:
        serialized_data = DesignatedRideSerializer(designated_ride).data

    return Response(serialized_data)


@api_view(http_method_names=['GET'])
def get_new_designation_for_driver(request, driver_id):
    designated_ride = DesignatedRide.objects.filter(driver_id=driver_id, status=DesignatedRide.Statuses.AWAITING).first()
    serialized_data = None

    if designated_ride:
        serialized_data = DesignatedRideSerializer(designated_ride).data

    return Response(serialized_data)


@api_view(http_method_names=['POST'])
def update_user_location(request):
    user_id = AuthenticationManager().get_user_id_or_none(headers=request.headers)
    if not user_id:
        raise NotAuthenticated()

    entry = {'user_id': user_id, 'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
             'latitude': request.data['latitude'], 'longitude': request.data['longitude']}
    GeoStorageManager.insert_one(entry)
    return Response({'status': 'success'})


@api_view(http_method_names=['GET'])
def get_latest_user_location(request, user_id):
    return Response({'geotag': GeoStorageManager.find_latest_user_location(user_id)})


@api_view(http_method_names=['PUT'])
def update_designated_ride_status(request, designated_ride_id):
    user_id = AuthenticationManager().get_user_id_or_none(headers=request.headers)
    if not user_id:
        raise NotAuthenticated()

    status = request.data['status']
    designated_ride = DesignatedRide.objects.get(id=designated_ride_id)
    designated_ride.status = status
    designated_ride.save()

    return Response({'status': 'success'})