from vrp import VRP
import utils


def to_console(vrp : VRP, name = 'VRP', stats = None):
    print(f'======== {name} ========')
    for ride in vrp.rides:
        print(f'Vehicle {ride.vehicle.id} serves orders {ride.nodes}')
    print(f'Total distance:', vrp.total_dist())
    if stats:
        print(f'Time elapsed:', utils.time_to_str(stats['time_elapsed']))