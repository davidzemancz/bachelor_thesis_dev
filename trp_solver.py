
import trp_solver_lp
import time

def solve_lp(trp, params):
    return solve(trp, trp_solver_lp, params)


def solve(trp, trp_solver, params):
    start_time = time.time()

    solved_trp, stats = trp_solver.solve(trp, params)

    end_time = time.time()
    time_elapsed = end_time - start_time
    
    return (solved_trp, { 'time_elapsed': time_elapsed } | stats)