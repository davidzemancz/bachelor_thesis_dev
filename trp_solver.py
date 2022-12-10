
import trp_solver_lp
import time

def solve_lp(trp):
    return solve(trp, trp_solver_lp)


def solve(trp, trp_solver):
    start_time = time.time()

    solved_trp = trp_solver.solve(trp)

    end_time = time.time()
    time_elapsed = end_time - start_time
    
    return (solved_trp, { 'time_elapsed': time_elapsed })