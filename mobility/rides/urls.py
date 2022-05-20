from django.urls import path

from . import views


urlpatterns = [
    path('rides/request/<int:pk>/', views.RideRequestReadUpdateDeleteAPIView.as_view(), name='ride-request-detail'),
    path('rides/request/create/', views.RideRequestListCreateAPIView.as_view(), name='ride-request-create'),

    path('rides/designated/<int:pk>/', views.DesignatedRideReadUpdateDeleteAPIView.as_view(), name='designated-ride-detail'),
    path('rides/designated/requested_ride/<int:requested_ride_id>/', views.get_designation_for_requested_ride, name='designation-for-requested_ride'),
    path('rides/designated/requested_ride_/driver/<int:driver_id>/', views.get_new_designation_for_driver, name='new-designation-for-driver'),

    path('ride/designated/status/<int:designated_ride_id>/', views.update_designated_ride_status, name='update-designated-ride-status'),
    path('rides/statuses/', views.get_designated_ride_statuses, name='rides-statuses'),
    path('location/update/', views.update_user_location, name='update-user-location'),
    path('location/get/<int:user_id>/', views.get_latest_user_location, name='get-user-location'),
]