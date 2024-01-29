# Create your views here.
from django.utils import timezone
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .features import BoundingBox
from .models import Route, Stop, StopTime
from .serializers import RouteSerializer, StopSerializer, RouteAndTripSerializer, StopTimeSerializer, \
    CoordinateSerializer


class RouteAndTripDetailView(generics.RetrieveAPIView):
    serializer_class = RouteAndTripSerializer
    lookup_field = 'id'

    def get_object(self):
        stop_time__stop_id = self.kwargs['pk']
        stop_time = StopTime.objects.get(stop_id=stop_time__stop_id)
        route = stop_time.trip.route
        trip = stop_time.trip
        return {'route': route, 'trip': trip}


class RouteListView(ListAPIView):
    serializer_class = RouteSerializer

    def get_queryset(self):
        stop_id = self.kwargs['stop_id']
        return Route.objects.filter(stop_id=stop_id)

def next_day_convert(time: str):
    hours = int(time[0]+time[1]) + 24
    return f"{hours}{time[2:]}"

class NextStopTimeListView(APIView):

    def get(self, request, stop_id, route_id):
        now = timezone.localtime(timezone.now()).time()
        stop_times = StopTime.objects.filter(
            stop_id=stop_id,
            trip__route_id=route_id,
            arrival_time__gte=now).prefetch_related('stop', 'trip')[:5]
        if len(stop_times) < 5:
            stop_times.union(StopTime.objects.filter(
                stop_id=stop_id,
                trip__route_id=route_id,
                arrival_time__gte="00:00:00").prefetch_related('stop', 'trip')[:5 - len(stop_times)])
            for stop_time in stop_times:
                stop_time.arrival_time = next_day_convert(stop_time.arrival_time)
        serializer = StopTimeSerializer(stop_times, many=True)
        times_data = serializer.data
        for i in range(times_data.__len__()):
            related_times = StopTime.objects.filter(
                trip_id=times_data[i]['trip']['id'],
                trip__times__id=times_data[i]['id']).prefetch_related('stop', 'trip', 'trip__route')
            times_data[i]['related_times'] = StopTimeSerializer(related_times, many=True).data

        return Response(serializer.data)


class StopListAreasView(APIView):
    def get(self, request, stop_area=None):
        if stop_area:
            stops: list[str] = Stop.objects.filter(stop_area__istartswith=stop_area).distinct(
                'stop_area').values_list('stop_area', flat=True)
        else:
            stops: list[str] = Stop.objects.all().distinct('stop_area').values_list('stop_area', flat=True)
        return Response(stops)


class StopListView(APIView):
    def get(self, request, stop_area):
        stops = Stop.objects.filter(stop_area__iexact=stop_area).order_by('stop_name')
        serializer = StopSerializer(stops, many=True)
        return Response(serializer.data)


class RouteListAPIView(APIView):
    def get(self, request, stop_id):
        stop = Stop.objects.get(id=stop_id)
        route_ids = Route.objects.filter(trips__times__stop=stop, trips__times__isnull=False).distinct('id').values_list('id', flat=True)
        routes = Route.objects.filter(id__in=route_ids).order_by('route_short_name')
        serializer = RouteSerializer(routes, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def coordinates_view(request):
    serializer = CoordinateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    longitude = serializer.validated_data['longitude']
    latitude = serializer.validated_data['latitude']
    bounding_box = BoundingBox(latitude, longitude, 10)
    stops = Stop.objects.filter(
        stop_lon__gte=bounding_box.min_longitude,
        stop_lon__lte=bounding_box.max_longitude,
        stop_lat__gte=bounding_box.min_latitude,
        stop_lat__lte=bounding_box.max_latitude,
    ).values()
    data = {
        'region': None,
        'nearest_stop': None,
        'stops': [],
    }
    if stops.__len__() == 0:
        return Response(data)
    stop = bounding_box.get_nearest_stop(stops)
    stops = Stop.objects.filter(stop_area__iexact=stop['stop_area']).order_by('stop_name')
    data = {
        'region': stop['stop_area'],
        'nearest_stop': stop,
        'stops': StopSerializer(stops, many=True).data,
    }
    return Response(data)
