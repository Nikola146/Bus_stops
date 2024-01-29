#from scipy.spatial import KDTree
import math

from api.models import Stop


class BoundingBox:
    latitude: float
    longitude: float


    @staticmethod
    def get_bounding_box(latitude, longitude, radius_in_kilometers):
        # Convert radius from kilometers to degrees
        radius_in_degrees = radius_in_kilometers / 111

        # Calculate minimum and maximum latitude
        min_latitude = latitude - radius_in_degrees
        max_latitude = latitude + radius_in_degrees

        # Calculate minimum and maximum longitude
        min_longitude = longitude - (radius_in_kilometers / (111 * math.cos(math.radians(latitude))))
        max_longitude = longitude + (radius_in_kilometers / (111 * math.cos(math.radians(latitude))))

        return min_latitude, max_latitude, min_longitude, max_longitude

    def __init__(self, latitude, longitude, radius_in_kilometers):
        min_latitude, max_latitude, min_longitude, max_longitude = self.get_bounding_box(latitude, longitude,
                                                                                         radius_in_kilometers)
        self.latitude = latitude
        self.longitude = longitude
        self.min_latitude = min_latitude
        self.max_latitude = max_latitude
        self.min_longitude = min_longitude
        self.max_longitude = max_longitude

    def __dict__(self):
        return {
            'longitude': self.latitude,
            'latitude': self.latitude,
            'min_latitude': self.min_latitude,
            'max_latitude': self.max_latitude,
            'min_longitude': self.min_longitude,
            'max_longitude': self.max_longitude
        }

    def get_nearest_stop(self, stops) -> dict:
        # Correct data format: a list of 2D points (tuples or lists with exactly two elements)
        data = [(stop['stop_lat'], stop['stop_lon']) for stop in stops]

        # Create a k-d tree from the stops list
     #   tree = KDTree(data)

        # Find the nearest stop to the given coordinates
     #   _, nearest_stop_index = tree.query((self.latitude, self.longitude))

        # Return the nearest stop
        return stops[0]

