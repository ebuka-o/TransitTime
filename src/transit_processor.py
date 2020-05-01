import sys, getopt
from data_manager import DataManager

def print_welcome_messaage():
    welcome_message ="""
******************************************************************

                      Welcome to TransitTime!                                             

******************************************************************

    """
    print(welcome_message)

def main(argv):
    
    # Default values
    bus_route_name = "MTABC_Q69"
    bus_stop_name = "21 ST/31 AV"

    help_text = """
    Given a bus route and stop name, returns the time it will take a bus to arrive
    at the stop and how far the bus is from the stop in miles.

    Usage: transit_processor.py -r <bus route> -s <bus stop>
    """
    try:
        # args can be ignored from getopts
        opts, _ = getopt.getopt(argv,"hr:s:",["help","route=","stop="])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(help_text)
            sys.exit()
        elif opt in ('-r', '--route'):
            bus_route_name = arg
        elif opt in ('-s', '--stop'):
            bus_stop_name = arg
        
    bus_route = DataManager.get_bus_route(bus_route_name, bus_stop_name, False)
    print_welcome_messaage()
    print(bus_route)

if __name__ == "__main__":
    main(sys.argv[1:])