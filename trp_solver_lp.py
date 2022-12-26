# https://developers.google.com/optimization/mip/mip_example
# https://google.github.io/or-tools/python/ortools/linear_solver/pywraplp.html

from pprint import pprint
from ortools.linear_solver import pywraplp
from trp import TRP, RoutePoint
import utils

def solve(trp : TRP, params):

    solver = pywraplp.Solver.CreateSolver('SCIP')
    INF = solver.infinity()
    LP_USE_EDGE_LB = 0.5
    edges = trp.edges()
    nodes = trp.nodes()
    vehicle_nodes = [vehicle.node for vehicle in trp.vehicles]


    # ----- Variables -----
    v_use_edge = {}
    v_edge_ind = {}
    for edge in edges:
        if params['lp_relaxation']:
            var = solver.NumVar(0, 1, str(edge))
        else:
            var = solver.IntVar(0, 1, str(edge))
        
        v_edge_ind[edge] = solver.IntVar(0, 1, "ind_" + str(edge))
        v_use_edge[edge] = var
    
    v_times = {}
    for node in nodes:
        var = solver.IntVar(0, INF, str(node))
        v_times[node] = var

    # ----- Constraints -----
    
    # 1) Routes must be continuous and cannot divide
    for node1 in nodes:
        for node2 in nodes:
            if node1 == node2 or node1 in vehicle_nodes: continue
            solver.Add(sum([v_use_edge[(node3, node1)] for node3 in nodes if node1 != node3]) >= v_use_edge[(node1, node2)])

    # 2) Vehicle can leave its original location using at most one edge
    for vehicle in trp.vehicles:
        solver.Add(sum([v_use_edge[(vehicle.node, node)] for node in nodes if node != vehicle.node]) <= 1)
        #solver.Add(sum([v_use_edge[(node3, vehicle.node)] for node3 in nodes if vehicle.node != node3]) == 0)

    # 3) Cycles are not allowed, just paths
    for node1 in nodes :
        #if node1 not in vehicle_nodes:
        solver.Add(sum([v_use_edge[(node1, node3)] for node3 in nodes if node1 != node3]) <= 1)
        solver.Add(sum([v_use_edge[(node3, node1)] for node3 in nodes if node1 != node3]) <= 1)

    # 4) Indicator of using edge (used for linear relaxation)
    for edge in edges:
        solver.Add(v_edge_ind[edge] >= v_use_edge[edge])
        solver.Add(v_edge_ind[edge] <= v_use_edge[edge] + (1 - 0.0001))

    # 4) Time
    for node1 in nodes:
        for node2 in nodes:
            if node1 == node2 or node2 in vehicle_nodes: continue
            M = 1000000
            edgeTravelTime = trp.travel_time(node1, node2)
            solver.Add(v_times[node1] + edgeTravelTime - M*(1 - v_edge_ind[(node1, node2)] ) <= v_times[node2])

    # 5) Time windows
    for request in trp.requests:
        solver.Add(v_times[request.nodeTo] <= request.twTo)
        solver.Add(v_times[request.nodeTo] >= request.twFrom)

    # Objective function
    solver.Maximize(sum([v_use_edge[var_key] * (trp.profit(var_key[0], var_key[1]) - trp.dist(var_key[0], var_key[1])) for var_key in v_use_edge]))
    
    # Solve
    if params['time_limit'] is not None: solver.SetTimeLimit(params['time_limit'] * 1000)
    if params['threads'] is not None: solver.SetNumThreads(params['threads'])
    status = solver.Solve()
    

    # Get solution if exists
    if status == pywraplp.Solver.INFEASIBLE: raise SystemError(f'Solution is INFEASIBLE')
    elif status == pywraplp.Solver.UNBOUNDED: raise SystemError(f'Solution is UNBOUNDED')
    elif status == pywraplp.Solver.ABNORMAL: raise SystemError(f'Solution is ABNORMAL')
    elif status == pywraplp.Solver.NOT_SOLVED: raise SystemError(f'Solution not been found yet')
    

    # Get routes
   
    routes_dict = {}
    for var_key in v_use_edge:
        edge_var = v_use_edge[var_key]
        value = edge_var.solution_value()
        if value > LP_USE_EDGE_LB:
            #if var_key[0] in routes_dict: raise SystemError(var_key[0]) ... ignored because of rounding issues
            routes_dict[var_key[0]] = var_key[1]

    #     if value>0:
    #         if var_key[0] not in routes_dict: 
    #             routes_dict[var_key[0]] = []
    #         routes_dict[var_key[0]].append((var_key[1],value))

    # pprint(routes_dict)
    # exit()

    objective_value = 0.0
    trp.routes = []
    for vehicle in trp.vehicles:
        route = [RoutePoint(vehicle.node, v_times[vehicle.node].solution_value())]

        while route[-1].node in routes_dict:
            node1 = route[-1].node
            node2 = routes_dict[route[-1].node]

            objective_value += trp.profit(node1, node2) - trp.dist(node1, node2)

            route.append(RoutePoint(node2, v_times[node2].solution_value()))

        if len(route) > 1: trp.routes.append(route)

    stats = { 'objective_value': objective_value }

    return trp, stats