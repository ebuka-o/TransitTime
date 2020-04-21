import json, requests
import time
from datetime import datetime
from pytz import timezone
from bus_monitor import BusRoute, Arrival

class DataManager:

    def __init__(self, key):
        self.key = key

    def get_bus_route(self, route_name, stop_name):
        pass

    