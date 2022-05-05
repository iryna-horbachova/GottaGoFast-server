from rest_framework.permissions import AllowAny
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CustomTokenObtainPairSerializer,
    ClientSerializer,
    ClientRegistrationSerializer,
    DriverSerializer,
    DriverRegistrationSerializer
)
from .models import (
    Client,
    Driver
)


class CustomTokenObtainPairAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class ClientListCreateAPIView(ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientRegistrationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class UserReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class DriverListCreateAPIView(ListCreateAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverRegistrationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class DriverReadUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer