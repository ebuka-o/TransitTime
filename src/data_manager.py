import time, logging
from datetime import datetime
from pytz import timezone
from bus_monitor import BusRoute, Arrival
from request_manager import Parser
from address_parser import AddressParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DataFormatter:
    @staticmethod
    def format_datetime(date_time, format):
        str_datetime = date_time.strftime(format)
        formatted_datetime = datetime.strptime(str_datetime, format)
        return formatted_datetime

    @staticmethod
    def format_time_without_ms(str_datetime):
        ms_separator_index = str_datetime.find('.')
        str_datetime = str_datetime[:ms_separator_index-1]
        return datetime.strptime(str_datetime, '%Y-%m-%dT%H:%M:%S')

class DataManager:
    @staticmethod
    def get_bus_route(route_name, stop_name, is_voice_command):
        if is_voice_command:
            stop_name = AddressParser.parse(stop_name)[0]
        logger.info(f"Bus name: {route_name}, stop name: {stop_name}")
        stop_code = DataManager.__get_stop_code(route_name, stop_name)
        logger.info(f"Stop code retrieved: {stop_code}")
        stop_monitoring_url = Parser.stop_monitoring_url(route_name, stop_code)
        stop_monitoring_json = Parser.make_request(stop_monitoring_url)
        bus_data_for_stop = DataManager.__get_bus_data_for_stop(stop_monitoring_json)
        return DataManager.__make_bus_route(route_name, stop_name, bus_data_for_stop)

    @staticmethod
    def __get_stop_code(route_name, stop_name):
        stops_url = Parser.stops_for_route_url(route_name)
        stops_json = Parser.make_request(stops_url)
        stops = stops_json["data"]["references"]["stops"]
        stop_code = list(filter(lambda stop: stop["name"] == stop_name, stops))[0]["code"]
        return stop_code
    
    @staticmethod
    def __make_bus_route(route_name, stop_name, bus_route_data):
        datetime_format = "%Y-%m-%d %H:%M:%S"
        curr_datetime = DataFormatter.format_datetime(datetime.now(timezone('US/Eastern')), 
        datetime_format)
        # populate bus route
        bus_route = BusRoute(route_name, stop_name)
        for bus_on_route in bus_route_data:
            minutes, seconds = DataManager.__get_bus_wait_time(bus_on_route, curr_datetime)
            if minutes == -1 and seconds == -1:
                continue
            distance = DataManager.__get_bus_dist_from_stop(bus_on_route)
            bus_route.add_bus_arrival((minutes, seconds), distance)
        return bus_route

    @staticmethod
    def __get_bus_arrival_time(bus_data):
        bus_arrival_time = ''
        bus_call_data = bus_data["MonitoredVehicleJourney"]["MonitoredCall"]
        if "ExpectedArrivalTime" in bus_call_data:
            bus_arrival_time = bus_call_data["ExpectedArrivalTime"]
            return DataFormatter.format_time_without_ms(bus_arrival_time)
        else:
            return None

    @staticmethod
    def __get_bus_wait_time(bus_data, curr_datetime):
        minutes, seconds = -1, -1
        bus_arrival_time = DataManager.__get_bus_arrival_time(bus_data)
        if bus_arrival_time is not None:
            currtime_ts = time.mktime(curr_datetime.timetuple())
            bustime_ts = time.mktime(bus_arrival_time.timetuple())
            time_diff = int(bustime_ts - currtime_ts)
            minutes = int(time_diff / 60)
            seconds = time_diff % 60
        return minutes, seconds

    @staticmethod
    def __get_bus_data_for_stop(stop_monitoring_json):
        return stop_monitoring_json["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]

    @staticmethod
    def __get_bus_dist_from_stop(bus_data):
        return bus_data["MonitoredVehicleJourney"]["MonitoredCall"]["Extensions"]["Distances"]["PresentableDistance"]
