from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views


urlpatterns = [
    path('token/', views.CustomTokenObtainPairAPIView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('user/id/', views.get_user_id, name='get-user-id'),

    path('clients/<int:pk>/', views.ClientReadUpdateDeleteAPIView.as_view(), name='client-detail'),
    path('clients/register/', views.ClientListCreateAPIView.as_view(), name='clients-register'),

    path('drivers/<int:pk>/', views.DriverReadUpdateDeleteAPIView.as_view(), name='driver-detail'),
    path('drivers/register/', views.DriverListCreateAPIView.as_view(), name='drivers-register'),
    path('drivers/active/', views.get_active_drivers, name='drivers-active'),
]