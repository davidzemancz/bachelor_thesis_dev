from trp import TRP, Request, Vehicle
import trp_drawer
import trp_gen
import trp_solver
import trp_printer

trp = trp_gen.generate(22, 3)

solved_trp, stats = trp_solver.solve_lp(trp)
trp_printer.to_console(solved_trp, 'TRP', stats)
trp_drawer.draw(trp)
