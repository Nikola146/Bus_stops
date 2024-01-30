from api.models import Trip, Route, Stop, StopTime
import csv

routes_path = 'gtfs/routes.txt'
stops_path = 'gtfs/stops.txt'
stop_times_path = 'gtfs/stop_times.txt'
trips_path = 'gtfs/trips.txt'

def run(*args):
    step = args[0]
    print(f"Running {step}...")
    if step == 'routes':
        return load_routes()
    elif step == 'trips':
        return load_trips()
    elif step == 'stops':
        return load_stops()
    elif step == 'stop_times':
        return load_stop_times()


def load_routes():
    filename = routes_path
    with open(filename, 'r') as file:
        lines = 9999
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            # Map CSV fields to model fields
            route_data = {
                'id': row['route_id'],
                'agency_id': row['agency_id'],
                'route_short_name': row['route_short_name'],
                'route_long_name': row['route_long_name'],
                'route_type': row['route_type'],
                'route_color': row['route_color'],
                'route_desc': row['route_desc'],
                'competent_authority': row['competent_authority'],
            }
            Route.objects.update_or_create(id=route_data['id'], defaults=route_data)
            print(f"Router {i}/{lines}")


def load_trips():
    filename = trips_path
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        lines = len(rows)
        for i, row in enumerate(rows):
            # Map CSV fields to model fields
            route_data = {
                'id': row['trip_id'],
                'route_id': row['route_id'],
                'service_id': row['service_id'],
                'trip_headsign': row['trip_headsign'],
                'trip_long_name': row['trip_long_name'],
                'direction_code': row['direction_code'],
            }
            Trip.objects.update_or_create(id=route_data['id'], defaults=route_data)
            print(f"Trip {i}/{lines}", end='\r')

def load_stops():
    filename = stops_path
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        lines = len(rows)
        new_items = []
        for i, row in enumerate(rows):
            # Map CSV fields to model fields
            new_item = {
                'id': row['stop_id'],
                'stop_name': row['stop_name'],
                'stop_code': row['stop_code'],
                'stop_lat': row['stop_lat'],
                'stop_lon': row['stop_lon'],
                'zone_id': row['zone_id'],
                'alias': row['alias'],
                'stop_area': row['stop_area'],
                'stop_desc': row['stop_desc'],
                'lest_x': row['lest_x'],
                'lest_y': row['lest_y'],
                'zone_name': row['zone_name'],
                'authority': row['authority'],
            }
            new_items.append(Stop(**new_item))
            print(f"Stop {i}/{lines}", end='\r')
        print("Bulk creating...")
        Stop.objects.bulk_create(new_items)


def load_stop_times():
    filename = stop_times_path
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        lines = len(rows)
        new_items = []
        for i, row in enumerate(rows):
            # Map CSV fields to model fields
            new_item = {
                'trip_id': row['trip_id'],
                'arrival_time': row['arrival_time'],
                'departure_time': row['departure_time'],
                'stop_id': row['stop_id'],
                'stop_sequence': row['stop_sequence'],
                'pickup_type': row['pickup_type'],
                'drop_off_type': row['drop_off_type'],
            }
            new_items.append(StopTime(**new_item))
            print(f"StopTime {i}/{lines}", end='\r')
            if len(new_items) > 50000:
                StopTime.objects.bulk_create(new_items)
                new_items = []
        
        StopTime.objects.bulk_create(new_items)

        print("Bulk creating...")
