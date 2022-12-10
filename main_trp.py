from trp import TRP, Request, Vehicle
import trp_drawer
import trp_gen

trp = trp_gen.generate(10, 3)
trp_drawer.draw(trp)
