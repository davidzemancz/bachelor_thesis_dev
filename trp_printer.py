from trp import TRP
import utils


def to_console(trp : TRP, name = 'TRP', stats = None):
    print(f'======== {name} ========')
    for request in trp.requests:
        print(f'Request {request.nodeFrom} -> {request.nodeTo}')
    for route in trp.routes:
        print(f'Route {[str(route_point.node) + " at " + str(route_point.minutes) for route_point in route]}')
    if stats:
        print(f'Time elapsed:', utils.time_to_str(stats['time_elapsed']))
        print(f'Objective value:', stats['objective_value'])