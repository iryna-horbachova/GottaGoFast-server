from django.contrib import admin

from . import models

class DesignatedRideAdmin(admin.ModelAdmin):
    list_display = ('driver_id', 'ride_request_id', 'price', 'status')

class RideRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'timestamp')


admin.site.register(models.DesignatedRide, DesignatedRideAdmin)
admin.site.register(models.RideRequest, RideRequestAdmin)
