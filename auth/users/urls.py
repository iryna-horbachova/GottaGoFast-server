from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path('token/', views.CustomTokenObtainPairAPIView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('client/<int:pk>/', views.ClientReadUpdateDeleteAPIView.as_view(), name='client-detail'),
    path('client/register/', views.ClientListCreateAPIView.as_view(), name='client-register'),

    path('driver/<int:pk>/', views.DriverReadUpdateDeleteAPIView.as_view(), name='driver-detail'),
    path('driver/register/', views.DriverListCreateAPIView.as_view(), name='driver-register'),
]