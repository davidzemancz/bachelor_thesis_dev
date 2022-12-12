import pprint
from trp import TRP, Request, Vehicle
import trp_drawer
import trp_gen
import trp_solver
import trp_printer
import random

params = {
    'lp_relaxation': True,
    'threads': 12,
    'time_limit': None
}

trp = trp_gen.generate(60, 8)
solved_trp, stats = trp_solver.solve_lp(trp, params)
trp_printer.to_console(solved_trp, 'TRP', stats)
trp_drawer.draw(solved_trp)

