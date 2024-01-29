import random
import string

from django.db import models


def generate_random_string():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=32))


# Create your models here.
class Route(models.Model):
    id = models.CharField(max_length=32, primary_key=True, default=generate_random_string)
    agency_id = models.IntegerField()
    route_short_name = models.CharField(max_length=32)
    route_long_name = models.CharField(max_length=1024)
    route_type = models.IntegerField()
    route_color = models.CharField(max_length=8)
    route_desc = models.TextField()
    competent_authority = models.CharField(max_length=64, null=True)

    class Meta:
        db_table = "routes"


class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='trips')
    service_id = models.IntegerField()
    trip_headsign = models.CharField(max_length=64)
    trip_long_name = models.CharField(max_length=1024)
    direction_code = models.CharField(max_length=32)

    class Meta:
        db_table = "trips"


class StopTime(models.Model):
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='times', null=True)
    arrival_time = models.CharField(max_length=8)
    departure_time = models.CharField(max_length=8)
    stop = models.ForeignKey('Stop', on_delete=models.CASCADE, related_name='times')
    stop_sequence = models.IntegerField()
    pickup_type = models.IntegerField()
    drop_off_type = models.IntegerField()

    class Meta:
        db_table = "stop_times"


class Stop(models.Model):
    stop_name = models.CharField(max_length=255, null=True, blank=True)
    stop_code = models.CharField(max_length=255, null=True, blank=True)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    zone_id = models.IntegerField()
    alias = models.CharField(max_length=255, null=True, blank=True)
    stop_area = models.CharField(max_length=255, null=True, blank=True)
    stop_desc = models.CharField(max_length=255, null=True, blank=True)
    lest_x = models.FloatField()
    lest_y = models.FloatField()
    zone_name = models.CharField(max_length=255, null=True, blank=True)
    authority = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "stops"
