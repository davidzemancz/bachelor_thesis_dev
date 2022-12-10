# https://developers.google.com/optimization/mip/mip_example
# https://google.github.io/or-tools/python/ortools/linear_solver/pywraplp.html

from ortools.linear_solver import pywraplp
from trp import TRP
import utils

def solve(trp : TRP):

    solver = pywraplp.Solver.CreateSolver('SCIP')

  

    return trp