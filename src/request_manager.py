import json, requests
from config import BUSTIME_API_KEY

class Parser:

    @staticmethod
    def make_request(url_request):
        request = requests.get(url_request)
        return request.json()

    @staticmethod
    def stops_for_route_url(route):
        return (
            f"http://bustime.mta.info/api/where/stops-for-route/{route}."
            f"json?key={BUSTIME_API_KEY}&includePolylines=false&version=2"
        )

    @staticmethod
    def stop_monitoring_url(route, stop_code):
        return (
            f"http://bustime.mta.info/api/siri/stop-monitoring.json?key={BUSTIME_API_KEY}&"
            f"OperatorRef=MTA&MonitoringRef={stop_code}&LineRef={route}"
        )