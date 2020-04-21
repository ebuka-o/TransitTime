import sys, getopt
import json, requests
import time
from datetime import datetime
from pytz import timezone

def get_stop_for_route_json(bus_route, api_key):
    stop_for_route_url = f"http://bustime.mta.info/api/where/stops-for-route/{bus_route}.json?key={api_key}&includePolylines=false&version=2"
    request = requests.get(stop_for_route_url)
    return request.json()

def get_stop_code(bus_route, stop_name, api_key):
    stop_for_route_json = get_stop_for_route_json(bus_route, api_key)
    stops = stop_for_route_json["data"]["references"]["stops"]
    stop_code = list(filter(lambda stop: stop["name"] == stop_name, stops))[0]["code"]
    return stop_code

def get_stop_monitoring_url(bus_route, stop_code, api_key):
    stop_monitoring_url = f"http://bustime.mta.info/api/siri/stop-monitoring.json?key={api_key}&OperatorRef=MTA&MonitoringRef={stop_code}&LineRef={bus_route}"
    request = requests.get(stop_monitoring_url)
    return request.json()

def format_arrival_time(arrival_time):
    ms_separator_index = arrival_time.find('.')
    arrival_time = arrival_time[:ms_separator_index-1]
    return datetime.strptime(arrival_time, '%Y-%m-%dT%H:%M:%S')

def get_time_away(bus, curr_datetime):
    bus_arrival_time = ''
    bus_call_data = bus["MonitoredVehicleJourney"]["MonitoredCall"]
    if "ExpectedArrivalTime" in bus_call_data:
        bus_arrival_time = bus_call_data["ExpectedArrivalTime"]
    else:
        # Ignore this entry
        return -1, -1
    bus_arrival_datetime = format_arrival_time(bus_arrival_time)
    currtime_ts = time.mktime(curr_datetime.timetuple())
    bustime_ts = time.mktime(bus_arrival_datetime.timetuple())
    time_diff = int(bustime_ts - currtime_ts)
    minutes = int(time_diff / 60)
    seconds = time_diff % 60
    return minutes, seconds

def format_time_and_distance(buses):
    curr_datetime = datetime.now(timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S')
    formatted_datetime = datetime.strptime(curr_datetime, '%Y-%m-%d %H:%M:%S')
    bus_stop_data = []
    for bus_on_route in buses:
        minutes, seconds = get_time_away(bus_on_route, formatted_datetime)
        if minutes == -1 and seconds == -1:
            continue
        distance = bus_on_route["MonitoredVehicleJourney"]["MonitoredCall"]["Extensions"]["Distances"]["PresentableDistance"]
        bus_stop_data.append({
            "minutes": minutes,
            "seconds": seconds,
            "distance": distance
        })
    return bus_stop_data

def get_arrival_time_and_distance_away(bus_route, stop_code, api_key):
    stop_monitoring_json = get_stop_monitoring_url(bus_route, stop_code, api_key)
    buses_on_route = stop_monitoring_json["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]
    return format_time_and_distance(buses_on_route)

def print_bus_stop_data(bus_stop_arrival_data, bus_route, bus_stop):
    bus_route_without_agency = bus_route[bus_route.find('_')+1:]
    bus_data = f"Bus route: {bus_route_without_agency}\nBus stop: {bus_stop}\n\n"
    if len(bus_stop_arrival_data) == 0:
        bus_data += f"No buses available at this time!"
    
    for index, data in enumerate(bus_stop_arrival_data):
        bus_data += f"Bus {index + 1} is {data['distance']} and arrives in {data['minutes']} "
        bus_data += f"minute(s) and {data['seconds']} second(s)!\n"
    print(bus_data)

def print_welcome_messaage():
    welcome_message ="""
******************************************************************

                      Welcome to TransitTime!                                             

******************************************************************

    """
    print(welcome_message)

def main(argv):
    
    # Default values
    bus_route = "MTABC_Q69"
    bus_stop = "21 ST/31 AV"

    help_text = """
    Given a bus route and stop name, returns the time it will take a bus to arrive
    at the stop and how far the bus is from the stop in miles.

    Usage: transit_processor.py -r <bus route> -s <bus stop> -k <access key>
    """
    try:
        opts, args = getopt.getopt(argv,"hr:s:k:",["help","route=","stop=","accesskey="])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_text)
            sys.exit()
        elif opt in ('-r', '--route'):
            bus_route = arg
        elif opt in ('-s', '--stop'):
            bus_stop = arg
        elif opt in ('-k', '--accesskey'):
            api_key = arg
    stop_code = get_stop_code(bus_route, bus_stop, api_key)
    bus_stop_arrival_data = get_arrival_time_and_distance_away(bus_route, stop_code, api_key)
    print_welcome_messaage()
    print_bus_stop_data(bus_stop_arrival_data, bus_route, bus_stop)

if __name__ == "__main__":
    main(sys.argv[1:])