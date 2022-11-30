from vrp import VRP,Ride,Vehicle,Order
import vrp_drawer
import vrp_solver
import vrp_printer
import vrp_gen

vrp = vrp_gen.generate(orders_count=10, vehicles_count=4)

solverd_vrp, stats = vrp_solver.solve_ortools(vrp.copy())
vrp_printer.to_console(solverd_vrp, name = 'OrTools', stats=stats)
vrp_drawer.draw(solverd_vrp)

solverd_vrp, stats = vrp_solver.solve_lp(vrp.copy())
vrp_printer.to_console(solverd_vrp, name = 'MIP', stats=stats)
vrp_drawer.draw(solverd_vrp)

