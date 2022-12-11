from trp import TRP
import utils


def to_console(trp : TRP, name = 'TRP', stats = None):
    print(f'======== {name} ========')
    for request in trp.requests:
        print(f'Request {request.nodeFrom} -> {request.nodeTo}')
    for route in trp.routes:
        print(f'Route {route}')
    if stats:
        print(f'Time elapsed:', utils.time_to_str(stats['time_elapsed']))