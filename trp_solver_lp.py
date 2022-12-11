# https://developers.google.com/optimization/mip/mip_example
# https://google.github.io/or-tools/python/ortools/linear_solver/pywraplp.html

from ortools.linear_solver import pywraplp
from trp import TRP
import utils

def solve(trp : TRP):

    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    edges = trp.edges()
    nodes = trp.nodes()
    vehicle_nodes = [vehicle.node for vehicle in trp.vehicles]


    # ----- Variables -----
    edge_vars = {}
    for edge in edges:
        var = solver.IntVar(0, 1, str(edge))
        edge_vars[edge] = var
    
    time_vars = {}
    for node in nodes:
        var = solver.IntVar(0, INF, str(node))
        time_vars[node] = var

    # ----- Constraints -----
    
    # 1) Routes must be continuous and cannot divide
    for node1 in nodes:
        for node2 in nodes:
            if node1 == node2 or node1 in vehicle_nodes: continue
            solver.Add(sum([edge_vars[(node3, node1)] for node3 in nodes if node1 != node3]) >= edge_vars[(node1, node2)])

    # 2) Vehicle can leave its original location using at most one edge
    for vehicle in trp.vehicles:
        solver.Add(sum([edge_vars[(vehicle.node, node)] for node in nodes if node != vehicle.node]) <= 1)
        #solver.Add(sum([edge_vars[(node3, vehicle.node)] for node3 in nodes if vehicle.node != node3]) == 0)

    # 3) Cycles are not allowed, just paths
    for node1 in nodes :
        if node1 not in vehicle_nodes:
            solver.Add(sum([edge_vars[(node1, node3)] for node3 in nodes if node1 != node3]) <= 1)
            solver.Add(sum([edge_vars[(node3, node1)] for node3 in nodes if node1 != node3]) <= 1)

    # 4) Time
    for node1 in nodes:
        for node2 in nodes:
            if node1 == node2 or node1 in vehicle_nodes or node2 in vehicle_nodes: continue
            M = 10000
            solver.Add(time_vars[node1] + trp.dist(node1, node2) - M*(1 - edge_vars[(node1, node2)]) <= time_vars[node2])

    # Objective function
    solver.Maximize(sum([edge_vars[var_key] * (trp.profit(var_key[0], var_key[1]) - trp.dist(var_key[0], var_key[1])) for var_key in edge_vars]))
    
    # Solve
    status = solver.Solve()
    stats = { 'objective_value': solver.Objective().Value() }

    # Get solution if exists
    if status == pywraplp.Solver.INFEASIBLE: raise SystemError(f'Solution is INFEASIBLE')
    elif status == pywraplp.Solver.UNBOUNDED: raise SystemError(f'Solution is UNBOUNDED')
    elif status == pywraplp.Solver.ABNORMAL: raise SystemError(f'Solution is ABNORMAL')
    elif status == pywraplp.Solver.NOT_SOLVED: raise SystemError(f'Solution not been found yet')
    
    for node in time_vars:
        print(node, time_vars[node].solution_value())

    # Get routes
    routes_dict = {}
    for var_key in edge_vars:
        edge_var = edge_vars[var_key]
        value = edge_var.solution_value()
        if value:
            if var_key[0] in routes_dict: print(var_key)
            routes_dict[var_key[0]] = var_key[1]
    
    for vehicle in trp.vehicles:
        route = [vehicle.node]

        while route[-1] in routes_dict:
            route.append(routes_dict[route[-1]])

        if len(route) > 1: trp.routes.append(route)


    return trp, stats