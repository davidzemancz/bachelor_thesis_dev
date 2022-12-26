from pprint import pprint
from trp import TRP, Request, Vehicle
import trp_drawer
import trp_gen
import trp_solver
import trp_printer
import random

def main():
    #test1()
    run(iters=5, vehicles=1, requests_per_tick=1)


def run(iters, vehicles, requests_per_tick):
    params = {
        'lp_relaxation': None,
        'threads': None,
        'time_limit': None
    }

    trp = trp_gen.generate(0, vehicles)
    for i in range(iters):
        print(f'----- Iteration {i} -----')
        for j in range(requests_per_tick):
            trp_gen.next_request(trp)
        
        params['lp_relaxation'] = False
        solved_trp, stats = trp_solver.solve_lp(trp, params)
        trp_printer.to_console(solved_trp, 'TRP LP-rel', stats)

        trp.tick()
        trp.update()

        


def test1():
    SEED = 245
    logs = []
    for i in range(20):
        params = {
            'lp_relaxation': True,
            'threads': None,
            'time_limit': None
        }

        trp = trp_gen.generate(10, 5, seed=i*SEED)
        solved_trp, statsLp = trp_solver.solve_lp(trp, params)
        trp_printer.to_console(solved_trp, 'TRP', statsLp)
        #trp_drawer.draw(solved_trp)

        params['lp_relaxation'] = False
        solved_trp, statsIp = trp_solver.solve_lp(trp, params)
        trp_printer.to_console(solved_trp, 'TRP', statsIp)

        logs.append((statsLp['objective_value'],statsIp['objective_value']))

    pprint(logs)

if __name__ == '__main__':
    main()