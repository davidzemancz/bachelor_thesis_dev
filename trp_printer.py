from trp import TRP
import utils


def to_console(trp : TRP, name = 'TRP', stats = None):
    print(f'======== {name} at {trp.minutes} ========')
    for request in trp.requests:
        print(f'Request {format_tuple(request.nodeFrom)} -> {format_tuple(request.nodeTo)} | {request.twFrom:.2f} - {request.twTo:.2f}')
    for route in trp.routes:
        print(f'Route {[str(format_tuple(route_point.node)) + " at " + str(route_point.minutes) for route_point in route]}')
    if stats:
        print(f'Time elapsed:', utils.time_to_str(stats['time_elapsed']))
        print(f'Objective value:', stats['objective_value'])

def format_tuple(tpl):
    return '('+','.join(format(f, '.2f') for f in tpl)+')'