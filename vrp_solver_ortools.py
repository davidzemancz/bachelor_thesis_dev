"""Simple Vehicles Routing Problem (VRP).

   This is a sample using the routing library python wrapper to solve a VRP
   problem.
   A description of the problem can be found here:
   http://en.wikipedia.org/wiki/Vehicle_routing_problem.

   Distances are in meters.
"""

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from vrp import VRP, Ride


def solve(vrp : VRP):
    """Entry point of the program."""

    # Create the routing index manager.
    locations_count = vrp.nodes_count
    vehicles_count = len(vrp.vehicles)
    depot = vrp.depot_node
    manager = pywrapcp.RoutingIndexManager(locations_count, vehicles_count, depot)
    
    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return vrp.dist(from_node, to_node)

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Distance constraint.
    dimension_name = 'Distance'
    routing.AddDimension(
        transit_callback_index,
        0,  # no slack
        3000,  # vehicle maximum travel distance
        True,  # start cumul to zero
        dimension_name)
    distance_dimension = routing.GetDimensionOrDie(dimension_name)
    distance_dimension.SetGlobalSpanCostCoefficient(100)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Get solution if exists
    if not solution:
        raise SystemError('Solution does not exists')
    
    vrp.rides = []
    for v_i in range(vehicles_count):
        
        ride_nodes = []
        index = routing.Start(v_i)
        while not routing.IsEnd(index):
            ride_nodes.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))

        ride_nodes.append(manager.IndexToNode(index))
        if len(ride_nodes) > 2:
            vrp.rides.append(Ride(vrp.vehicles[v_i], ride_nodes))
    
    return vrp


if __name__ == '__main__':
    solve()