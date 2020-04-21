import time
from datetime import datetime
from pytz import timezone
from bus_monitor import BusRoute, Arrival
from request_manager import Parser

class DataManager:

    def __init__(self, key):
        self.key = key

    def get_stop_code(self, route_name, stop_name):
        stops_url = Parser.stops_for_route_url(route_name, self.key)
        stops_json = Parser.make_request(stops_url)
        stops = stops_json["data"]["references"]["stops"]
        stop_code = list(filter(lambda stop: stop["name"] == stop_name, stops))[0]["code"]
        return stop_code

    def get_bus_route(self, route_name, stop_name):
        pass