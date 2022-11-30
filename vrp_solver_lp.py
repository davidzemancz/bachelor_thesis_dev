# https://developers.google.com/optimization/mip/mip_example
# https://google.github.io/or-tools/python/ortools/linear_solver/pywraplp.html

from ortools.linear_solver import pywraplp
from vrp import VRP, Ride
import utils

def solve(vrp : VRP):

    vehicles_count = len(vrp.vehicles)

    solver = pywraplp.Solver.CreateSolver('SCIP')

    # Variables
    edge_vars = {} # variable determining wheather use uv-edge 
    for u in range(vrp.nodes_count):
        for v in range(vrp.nodes_count):
            if u == v: continue

            var_key = (u, v)
            var = solver.BoolVar(str(var_key))
            edge_vars[var_key] = var
    node_vars = {} # aditional variables for subtour elimination
    for u in range(1, vrp.nodes_count):
        var_key = (u)
        var = solver.IntVar(1, vrp.nodes_count - 1, str(var_key))
        node_vars[var_key] = var

    # Constraints (https://en.wikipedia.org/wiki/Vehicle_routing_problem#Vehicle_flow_formulations)
    # 1) Each node is entered once (except depot)
    for order1 in vrp.orders:
        solver.Add(sum([edge_vars[var_key] for var_key in edge_vars if var_key[1] == order1.node]) == 1)

    # 2) Each node is leaved once (except depot)
    for order1 in vrp.orders:
        solver.Add(sum([edge_vars[var_key] for var_key in edge_vars if var_key[0] == order1.node]) == 1)

    # 3) Number of vehicles leaving depot is equal to number of arriving ones
    solver.Add(sum([edge_vars[var_key] for var_key in edge_vars if var_key[0] != vrp.depot_node and var_key[1] == vrp.depot_node]) == sum([edge_vars[var_key] for var_key in edge_vars if var_key[0] == vrp.depot_node and var_key[1] != vrp.depot_node]))
    solver.Add(sum([edge_vars[var_key] for var_key in edge_vars if var_key[0] != vrp.depot_node and var_key[1] == vrp.depot_node]) <= vehicles_count)
    solver.Add(sum([edge_vars[var_key] for var_key in edge_vars if var_key[0] == vrp.depot_node and var_key[1] != vrp.depot_node]) <= vehicles_count)

    # 4) Subtour elimination constraints (Dantzig formulation)
    # pwr_set = utils.powerset([(i + 1) for i in range(vrp.nodes_count - 1)])
    # for subset in pwr_set:
    #     if len(subset) > 0:
    #         solver.Add(sum([edge_vars[var_key] for var_key in edge_vars if var_key[0] not in subset and var_key[1] in subset]) >= 1)

    # 4) Subtour elimination constraints (MTZ (Muller, Tucker, Zemlin) formulation)
    for order1 in vrp.orders:
        for order2 in vrp.orders:
            if order1.id == order2.id: continue
            solver.Add(node_vars[(order1.node)] - node_vars[(order2.node)] + ((vrp.nodes_count - 1) * edge_vars[(order1.node, order2.node)]) <= vrp.nodes_count - 2)

    # # 5) Capacity constraints
    # for vehicle in vrp.vehicles:
    #     solver.Add(sum([edge_vars[var_key]*vrp.order(var_key[1]).demand for var_key in edge_vars if var_key[1] != vrp.depot_node and var_key[2] == vehicle.id]) <= vehicle.capacity)


    # 6) Vehicle is used at most once
    # for order1 in vrp.orders:
    #     for order2 in vrp.orders:
    #         solver.Add(sum([edge_vars[var_key] for var_key in edge_vars if var_key[0] == order1.node and var_key[1] == order2.node]) <= 1)

    # Objective function
    solver.Minimize(sum([edge_vars[var_key] * vrp.dist(var_key[0], var_key[1]) for var_key in edge_vars]))

    # solver.SetTimeLimit(60 * 1000)
    # solver.SetNumThreads(8)
    status = solver.Solve()

    # Get solution if exists
    if status == pywraplp.Solver.INFEASIBLE: raise SystemError(f'Solution is INFEASIBLE')
    elif status == pywraplp.Solver.UNBOUNDED: raise SystemError(f'Solution is UNBOUNDED')
    elif status == pywraplp.Solver.ABNORMAL: raise SystemError(f'Solution is ABNORMAL')
    elif status == pywraplp.Solver.NOT_SOLVED: raise SystemError(f'Solution not been found yet')

    successors = {}
    for var_key in edge_vars:
        edge_var = edge_vars[var_key]
        value = edge_var.solution_value()
        
        if value:
            if successors.get(var_key[0]) is None: successors[var_key[0]] = []
            successors[var_key[0]].append(var_key[1])


    vrp.rides = []
    for succ in successors[vrp.depot_node]:
        ride_nodes = [vrp.depot_node]
        ride_nodes.append(succ)
        while succ != vrp.depot_node:
            succ = successors[succ][0]
            ride_nodes.append(succ)
        vrp.rides.append(Ride(vrp.vehicles[0], ride_nodes))

    return vrp