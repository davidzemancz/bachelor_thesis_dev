from pprint import pprint
from trp import TRP, Request, Vehicle
import trp_drawer
import trp_gen
import trp_solver
import trp_printer
import random

def main():
    test1()

def test1():
    params = {
        'lp_relaxation': True,
        'threads': 12,
        'time_limit': None
    }

    trp = trp_gen.generate(40, 30)
    solved_trp, stats = trp_solver.solve_lp(trp, params)
    trp_printer.to_console(solved_trp, 'TRP', stats)
    trp_drawer.draw(solved_trp)

    params['lp_relaxation'] = False
    solved_trp, stats = trp_solver.solve_lp(trp, params)
    trp_printer.to_console(solved_trp, 'TRP', stats)
    trp_drawer.draw(solved_trp)

def test2():
    SEED = 111
    logs = []
    for i in range(20):
        params = {
            'lp_relaxation': True,
            'threads': 12,
            'time_limit': 60
        }

        trp = trp_gen.generate(40, 3, seed=i*SEED)
        solved_trp, statsLp = trp_solver.solve_lp(trp, params)
        trp_printer.to_console(solved_trp, 'TRP', statsLp)
        

        params['lp_relaxation'] = False
        solved_trp, statsIp = trp_solver.solve_lp(trp, params)
        trp_printer.to_console(solved_trp, 'TRP', statsIp)

        logs.append((statsLp['objective_value'],statsIp['objective_value']))

    pprint(logs)

if __name__ == '__main__':
    main()