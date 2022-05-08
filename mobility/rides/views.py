from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import (
    RideRequest,
    DesignatedRide
)
from .serializers import (
    RideRequestSerializer,
    DesignatedRideSerializer
)
from .services import AuthenticationManager


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

    return Response({'designated_ride': serialized_data})


@api_view(http_method_names=['GET'])
def get_new_designation_for_driver(request, driver_id):
    designated_ride = DesignatedRide.objects.filter(driver_id=driver_id, status=DesignatedRide.Statuses.AWAITING).first()
    serialized_data = None

    if designated_ride:
        serialized_data = DesignatedRideSerializer(designated_ride).data

    return Response({'designated_ride': serialized_data})
