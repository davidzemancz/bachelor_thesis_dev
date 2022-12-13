import utils
import random
from trp import TRP,Vehicle,Request

GRID_SIZE = 1000

def generate(requests_count, vehicles_count, seed = None, dist = None) -> TRP:
    
    if dist is None: dist = lambda x, y: utils.eclidean_norm(x, y) 
    trp = TRP(dist, 0)

    if seed: random.seed(seed)

    for v_i in range(1, vehicles_count + 1):
        node = (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE))
        trp.vehicles.append(Vehicle(v_i, node))

    for _ in range(1, requests_count + 1):
      trp.requests.append(get_request(trp))

    return trp


def next_request(trp : TRP) -> TRP:
    trp.requests.append(get_request(trp))
    return trp



def get_request(trp) -> Request:
    nodeFrom = (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE))
    nodeTo = (random.randint(0, GRID_SIZE), random.randint(0, GRID_SIZE))
    profit = 5 * trp.dist(nodeFrom, nodeTo)
    twFrom = trp.time + random.randint(1, 3)
    twTo = twFrom + random.randint(1, 3)
    return Request(len(trp.requests) + 1, nodeFrom, nodeTo, profit, twFrom, twTo)
    