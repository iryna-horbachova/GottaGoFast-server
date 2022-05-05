from django.urls import path

from . import views


urlpatterns = [
    path('rides/request/<int:pk>/', views.RideRequestReadUpdateDeleteAPIView.as_view(), name='ride-request-detail'),
    path('rides/request/create/', views.RideRequestListCreateAPIView.as_view(), name='ride-request-create'),

    path('rides/designated/<int:pk>/', views.DesignatedRideReadUpdateDeleteAPIView.as_view(), name='designated-ride-detail'),
    path('rides/statuses/', views.get_designated_ride_statuses, name='rides-statuses'),
]