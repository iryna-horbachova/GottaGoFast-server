from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated

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