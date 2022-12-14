from pprint import pprint
from trp import TRP, Request, Vehicle
import trp_drawer
import trp_gen
import trp_solver
import trp_printer
import random

def main():
    test2()

def test3():
    params = {
        'lp_relaxation': True,
        'threads': 1,
        'time_limit': None
    }
    trp = trp_gen.generate(10, 5)

    for run in range(10):
        trp = trp_gen.next_request(trp)
        solved_trp, stats = trp_solver.solve_lp(trp, params)
        trp_printer.to_console(solved_trp, 'TRP', stats)
        trp_drawer.draw(solved_trp)


def test2():
    params = {
        'lp_relaxation': True,
        'threads': None,
        'time_limit': None
    }

    trp = trp_gen.generate(10, 5)
    solved_trp, stats = trp_solver.solve_lp(trp, params)
    trp_printer.to_console(solved_trp, 'TRP', stats)
    trp_drawer.draw(solved_trp)

    # params['lp_relaxation'] = False
    # solved_trp, stats = trp_solver.solve_lp(trp, params)
    # trp_printer.to_console(solved_trp, 'TRP', stats)
    # trp_drawer.draw(solved_trp)

def test1():
    SEED = 208
    logs = []
    for i in range(20):
        params = {
            'lp_relaxation': True,
            'threads': None,
            'time_limit': 10
        }

        trp = trp_gen.generate(20, 8, seed=i*SEED)
        solved_trp, statsLp = trp_solver.solve_lp(trp, params)
        trp_printer.to_console(solved_trp, 'TRP', statsLp)

        params['lp_relaxation'] = False
        solved_trp, statsIp = trp_solver.solve_lp(trp, params)
        trp_printer.to_console(solved_trp, 'TRP', statsIp)

        logs.append((statsLp['objective_value'],statsIp['objective_value']))

    pprint(logs)

if __name__ == '__main__':
    main()