class Arrival:

    def __init__(self, time_from_stop, dist_from_stop):
        self.time_from_stop = time_from_stop
        self.dist_from_stop = dist_from_stop

    def __repr__(self):
        return f'''{self.__class__.__name__}(
        {self.time_from_stop!r}, {self.dist_from_stop!r})'''
    
    def __str__(self):
        return (
            f'{self.dist_from_stop} and arrives in {self.get_minutes()} '
            f'minutes and {self.get_seconds()} seconds'
        )

    def get_minutes(self):
        return self.time_from_stop[0]

    def get_seconds(self):
        return self.time_from_stop[1]

class BusRoute:

    def __init__(self, bus_route_name, bus_stop):
        self.name = bus_route_name
        self.monitored_stop = bus_stop
        self.bus_arrivals = []

    def add_bus_arrival(self, time, distance):
        self.bus_arrivals.append(Arrival(time, distance))

    def get_short_bus_route_name(self, long_route_name):
        return long_route_name[long_route_name.rfind('_')+1:]

    def __repr__(self):
        return f'''{self.__class__.__name__}(
        {self.name!r}, {self.monitored_stop!r}, {self.bus_arrivals!r})'''
    
    def __str__(self):
        bus_str = (
            f'For the {self.get_short_bus_route_name(self.name)} bus '
            f'at the {self.monitored_stop} stop, '
        )
        if len(self.bus_arrivals) == 0:
            bus_str += f'there are no buses available at this time!'
        for index, arrival in enumerate(self.bus_arrivals):
            bus_str += f'{self.ordinal(index + 1)} bus is {arrival}, '

        # excluding trailing characters
        return bus_str[:-2]

    def ordinal(self, num):
        return BusRoute.ordinal_dict.get(num, "next")
        
    ordinal_dict = {
        1 : "first",
        2 : "second",
        3 : "third"
    }
