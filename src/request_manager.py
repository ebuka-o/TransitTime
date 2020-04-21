import json, requests

class Parser:

    @staticmethod
    def make_request(url_request):
        request = requests.get(url_request)
        return request.json()

    @staticmethod
    def stops_for_route_url(route, key):
        return (
            f"http://bustime.mta.info/api/where/stops-for-route/{route}."
            f"json?key={key}&includePolylines=false&version=2"
        )

    @staticmethod
    def stop_monitoring_url(route, stop_code, key):
        return (
            f"http://bustime.mta.info/api/siri/stop-monitoring.json?key={key}&"
            f"OperatorRef=MTA&MonitoringRef={stop_code}&LineRef={route}"
        )