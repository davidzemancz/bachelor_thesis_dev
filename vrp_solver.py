
import vrp_solver_lp
import vrp_solver_ortools
import time

def solve_lp(vrp):
    return solve(vrp, vrp_solver_lp)

def solve_ortools(vrp):
    return solve(vrp, vrp_solver_ortools)


def solve(vrp, vrp_solver):
    start_time = time.time()

    solved_vrp = vrp_solver.solve(vrp)

    end_time = time.time()
    time_elapsed = end_time - start_time
    
    return (solved_vrp, { 'time_elapsed': time_elapsed })