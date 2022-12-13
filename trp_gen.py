import utils
import random
from trp import TRP,Vehicle,Request

def generate(requests_count, vehicles_count, seed = None, dist = None) -> TRP:
    UP = 1000

    if dist is None: dist = lambda x, y: utils.eclidean_norm(x, y) 
    trp = TRP(requests_count, dist)

    if seed: random.seed(seed)

    for v_i in range(1, vehicles_count + 1):
        node = (random.randint(0, UP), random.randint(0, UP))
        trp.vehicles.append(Vehicle(v_i, node))

    for r_i in range(1, requests_count + 1):
        nodeFrom = (random.randint(0, UP), random.randint(0, UP))
        nodeTo = (random.randint(0, UP), random.randint(0, UP))
        profit = 5 * dist(nodeFrom, nodeTo)
        twFrom = random.randint(1, 3)
        twTo = twFrom + random.randint(1, 3)
        trp.requests.append(Request(r_i, nodeFrom, nodeTo, profit, twFrom, twTo))

    return trp

