from rest_framework import serializers

from api.models import Route, Stop, Trip, StopTime


class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ('id', 'agency_id', 'route_short_name', 'route_long_name', 'route_type', 'route_color', 'route_desc',
                  'competent_authority')


class TripSerializer(serializers.ModelSerializer):
    route = RouteSerializer()

    class Meta:
        model = Trip
        fields = ['id', 'route', 'service_id', 'trip_headsign', 'trip_long_name', 'direction_code']


class StopTimeSerializer(serializers.ModelSerializer):
    stop = StopSerializer()
    trip = TripSerializer()

    class Meta:
        model = StopTime
        fields = '__all__'


class RouteAndTripSerializer(serializers.Serializer):
    route = RouteSerializer()
    trip = TripSerializer()


class CoordinateSerializer(serializers.Serializer):
    longitude = serializers.FloatField(min_value=-180, max_value=180)
    latitude = serializers.FloatField(min_value=-90, max_value=90)
